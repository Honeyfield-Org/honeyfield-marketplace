#!/usr/bin/env python3
"""Abgleich der Tool-Map des Plugins honeyfield-marketing-mcp mit dem Server.

Hintergrund: Die Tool-Map (plugins/honeyfield-marketing-mcp/references/tool-map.md)
ist die einzige vollstaendige Tool-Referenz der Skills. Sie lief wiederholt dem
Server hinterher (Runde 7: 27 registrierte Tools fehlten, 11/2026: 16 fehlten).
Der Server-Code (ads-mcp-platform) ist privat, dieses Repo oeffentlich. Deshalb
liegt ein Schnappschuss der Server-Registry im Repo:

  .github/tool-registry/honeyfield-marketing-mcp.json
    tools   {name: {source, write, doc_sha}}  aus mcp-server/tenancy/permissions.py
                                               (TOOL_REGISTRY) + Docstring-Hash aus
                                               mcp-server/api/*.py
    prompts [name]                             aus den @mcp.prompt-Dekoratoren in api/

Pruefen (Default, laeuft in CI):
  python3 .github/scripts/check_tool_map.py
    - jedes Tool aus dem Schnappschuss steht in der Tool-Map (fehlend = Fehler)
    - kein Tool-Map-Eintrag ohne Server-Tool (tot = Fehler; Ausnahme: die
      OAuth-Pseudo-Tools authenticate/complete_authentication des Plugin-Kontexts)
    - R/W-Spalte passt zur Registry (W-Tools: W oder R/W, R-Tools: R)
    - jeder MCP-Prompt steht im Abschnitt "## MCP-Prompts" und umgekehrt
    - die Tool-Zahl im README stimmt

Schnappschuss erneuern (lokal, braucht einen Checkout von ads-mcp-platform):
  python3 .github/scripts/check_tool_map.py --update ~/development/ads-mcp-platform [--rev origin/main]
    Liest permissions.py und api/*.py per `git show <rev>:...` (vorher `git fetch`),
    schreibt den Schnappschuss neu und listet neue, entfernte und Tools mit
    geaendertem Docstring. Genau diese Zeilen der Tool-Map gegen die Docstrings
    pruefen; danach ohne --update laufen lassen.
"""
import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys

TOOL_MAP = "plugins/honeyfield-marketing-mcp/references/tool-map.md"
SNAPSHOT = ".github/tool-registry/honeyfield-marketing-mcp.json"
README = "README.md"
PSEUDO_TOOLS = {"authenticate", "complete_authentication"}
PROMPT_SECTION = "## MCP-Prompts"
ROW = re.compile(r"^\| `([a-z0-9_]+)` \|")
README_COUNT = re.compile(r"\((\d+) Tools über (\d+) Quellen")


# ── Schnappschuss aus ads-mcp-platform erzeugen ──────────────────────────


def _git_show(repo, rev, path):
    return subprocess.check_output(["git", "-C", repo, "show", f"{rev}:{path}"], text=True)


def _registry(src):
    tree = ast.parse(src)
    ns, reg = {}, None
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
        elif isinstance(node, ast.AnnAssign):
            target = node.target
        else:
            continue
        if not isinstance(target, ast.Name):
            continue
        if target.id == "TOOL_REGISTRY":
            reg = node.value
            continue
        try:
            ns[target.id] = ast.literal_eval(node.value)
        except (ValueError, SyntaxError):
            pass
    if not isinstance(reg, ast.Dict):
        sys.exit("TOOL_REGISTRY nicht gefunden")
    tools = {}
    for key, value in zip(reg.keys, reg.values):
        source_node, write_node = value.elts
        if isinstance(source_node, ast.Name):
            source = ns[source_node.id]
        else:
            source = ast.literal_eval(source_node)
        if isinstance(source, tuple):
            source = list(source)
        tools[ast.literal_eval(key)] = {"source": source, "write": ast.literal_eval(write_node)}
    return tools


def _api(repo, rev):
    files = subprocess.check_output(
        ["git", "-C", repo, "ls-tree", "--name-only", rev, "mcp-server/api/"], text=True
    ).split()
    docs, prompts = {}, set()
    for path in files:
        if not path.endswith(".py"):
            continue
        tree = ast.parse(_git_show(repo, rev, path))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for deco in node.decorator_list:
                text = ast.unparse(deco)
                name = node.name
                if isinstance(deco, ast.Call):
                    for kw in deco.keywords:
                        if kw.arg == "name":
                            name = ast.literal_eval(kw.value)
                if text.startswith("mcp.tool"):
                    docs[name] = ast.get_docstring(node) or ""
                elif text.startswith("mcp.prompt"):
                    prompts.add(name)
    return docs, sorted(prompts)


def _dump(snapshot):
    """Eine Zeile je Tool: kleine, gut lesbare Diffs beim Erneuern."""
    zeilen = [f"  {json.dumps(n, ensure_ascii=False)}: {json.dumps(e, ensure_ascii=False)}"
              for n, e in snapshot["tools"].items()]
    return (
        "{\n"
        f'  "quelle": {json.dumps(snapshot["quelle"], ensure_ascii=False)},\n'
        f'  "anzahl_tools": {snapshot["anzahl_tools"]},\n'
        f'  "prompts": {json.dumps(snapshot["prompts"], ensure_ascii=False)},\n'
        '  "tools": {\n  ' + ",\n  ".join(zeilen) + "\n  }\n}\n"
    )


def update(repo, rev):
    tools = _registry(_git_show(repo, rev, "mcp-server/tenancy/permissions.py"))
    docs, prompts = _api(repo, rev)
    ohne_doc = sorted(set(tools) - set(docs))
    ohne_reg = sorted(set(docs) - set(tools))
    if ohne_doc or ohne_reg:
        print(f"Warnung: Registry ohne Wrapper {ohne_doc}, Wrapper ohne Registry {ohne_reg}")
    for name, entry in tools.items():
        doc = docs.get(name, "")
        entry["doc_sha"] = hashlib.sha256(doc.encode("utf-8")).hexdigest()[:12]
    sha = subprocess.check_output(["git", "-C", repo, "rev-parse", "--short", rev], text=True).strip()

    alt = {}
    if os.path.isfile(SNAPSHOT):
        with open(SNAPSHOT, encoding="utf-8") as f:
            alt = json.load(f)
    alt_tools = alt.get("tools", {})
    neu = sorted(set(tools) - set(alt_tools))
    weg = sorted(set(alt_tools) - set(tools))
    geaendert = sorted(
        n for n in tools if n in alt_tools and alt_tools[n].get("doc_sha") != tools[n]["doc_sha"]
    )
    rw = sorted(n for n in tools if n in alt_tools and alt_tools[n].get("write") != tools[n]["write"])

    snapshot = {
        "quelle": f"ads-mcp-platform {sha} (mcp-server/tenancy/permissions.py + mcp-server/api)",
        "anzahl_tools": len(tools),
        "tools": dict(sorted(tools.items())),
        "prompts": prompts,
    }
    os.makedirs(os.path.dirname(SNAPSHOT), exist_ok=True)
    with open(SNAPSHOT, "w", encoding="utf-8") as f:
        f.write(_dump(snapshot))
    print(f"Schnappschuss {SNAPSHOT}: {len(tools)} Tools, {len(prompts)} Prompts (Stand {sha})")
    for label, names in (
        ("neu", neu),
        ("entfernt", weg),
        ("Docstring geaendert", geaendert),
        ("R/W geaendert", rw),
    ):
        if names:
            print(f"  {label} ({len(names)}): {', '.join(names)}")
    return 0


# ── Tool-Map pruefen ─────────────────────────────────────────────────────


def _cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def parse_map(text):
    tools, prompts, dups = {}, set(), []
    in_prompts = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_prompts = line.startswith(PROMPT_SECTION)
            continue
        m = ROW.match(line)
        if not m:
            continue
        name = m.group(1)
        if in_prompts:
            prompts.add(name)
        else:
            if name in tools:
                dups.append(name)
            tools[name] = _cells(line)[-1]
    return tools, prompts, dups


def check():
    with open(SNAPSHOT, encoding="utf-8") as f:
        snap = json.load(f)
    with open(TOOL_MAP, encoding="utf-8") as f:
        tools, prompts, dups = parse_map(f.read())
    reg = snap["tools"]
    fehler = []

    fehlend = sorted(set(reg) - set(tools))
    tot = sorted(set(tools) - set(reg) - PSEUDO_TOOLS)
    if fehlend:
        fehler.append(f"{len(fehlend)} Server-Tools fehlen in der Tool-Map: {', '.join(fehlend)}")
    if tot:
        fehler.append(f"{len(tot)} Tool-Map-Eintraege ohne Server-Tool: {', '.join(tot)}")
    if dups:
        fehler.append(f"Doppelte Tool-Map-Eintraege: {', '.join(sorted(set(dups)))}")
    for name in sorted(set(reg) & set(tools)):
        rw = tools[name]
        erlaubt = {"W", "R/W"} if reg[name]["write"] else {"R"}
        if rw not in erlaubt:
            fehler.append(f"R/W-Spalte von {name} ist {rw!r}, Registry sagt {'W' if reg[name]['write'] else 'R'}")

    p_fehlend = sorted(set(snap.get("prompts", [])) - prompts)
    p_tot = sorted(prompts - set(snap.get("prompts", [])))
    if p_fehlend:
        fehler.append(f"MCP-Prompts fehlen im Abschnitt {PROMPT_SECTION!r}: {', '.join(p_fehlend)}")
    if p_tot:
        fehler.append(f"Prompt-Eintraege ohne Server-Prompt: {', '.join(p_tot)}")

    if os.path.isfile(README):
        with open(README, encoding="utf-8") as f:
            m = README_COUNT.search(f.read())
        quellen = set()
        for entry in reg.values():
            src = entry["source"]
            quellen.update(src if isinstance(src, list) else [src] if src else [])
        if not m:
            fehler.append("README: Angabe '(<N> Tools über <M> Quellen' nicht gefunden")
        elif (int(m.group(1)), int(m.group(2))) != (len(reg), len(quellen)):
            fehler.append(
                f"README nennt {m.group(1)} Tools über {m.group(2)} Quellen, "
                f"Server hat {len(reg)} Tools über {len(quellen)} Quellen"
            )

    if fehler:
        print("Tool-Map nicht im Abgleich mit dem Server-Schnappschuss:")
        for f_ in fehler:
            print(f"  - {f_}")
        print(f"(Schnappschuss: {snap.get('quelle')})")
        return 1
    print(
        f"Tool-Map im Abgleich: {len(reg)} Tools, {len(snap.get('prompts', []))} Prompts "
        f"({snap.get('quelle')})"
    )
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--update", metavar="ADS_MCP_PLATFORM", help="Schnappschuss aus diesem Checkout erneuern")
    parser.add_argument("--rev", default="origin/main", help="Revision in ads-mcp-platform (Default origin/main)")
    args = parser.parse_args()
    if args.update:
        return update(os.path.expanduser(args.update), args.rev)
    return check()


if __name__ == "__main__":
    sys.exit(main())
