#!/usr/bin/env python3
"""Generiert KI-Bilder über die fal.ai-Queue-API.

Usage:
    python3 generate_image.py \
        --prompt "..." \
        --aspect-ratio "16:9" \
        --resolution "1K" \
        --output "pfad/zum/bild.png"

    Optional:
        --model "fal-ai/nano-banana-pro"   (Default)
        --num-images 1                      (Default)

Environment:
    FAL_KEY muss als Shell-Umgebungsvariable gesetzt sein:
        export FAL_KEY="<key-id>:<key-secret>"
    Bewusst kein .env-Loading — Marketplace-Repo, kein Key im Repo.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

POLL_INTERVAL = 2
TIMEOUT = 180


def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def request_json(url, headers, data=None, timeout=30):
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        die(f"API-Fehler {e.code}: {body}")
    except urllib.error.URLError as e:
        die(f"Netzwerk-Fehler: {e.reason}")
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        die(f"Ungültige API-Antwort (kein JSON): {body[:500]}")


def poll_for_result(status_url, response_url, headers):
    start = time.time()
    while time.time() - start < TIMEOUT:
        status = request_json(status_url, headers)
        state = status.get("status", "")
        if state == "COMPLETED":
            return request_json(response_url, headers)
        if state in ("FAILED", "CANCELLED"):
            die(f"Generierung fehlgeschlagen: {json.dumps(status, indent=2)}")
        print(f"  Status: {state} (Queue-Position: {status.get('queue_position', '?')})")
        time.sleep(POLL_INTERVAL)
    die("Timeout beim Warten auf die Generierung.")


def main():
    parser = argparse.ArgumentParser(description="KI-Bilder via fal.ai generieren")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--aspect-ratio", default="16:9",
                        help="1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4, 21:9")
    parser.add_argument("--resolution", default="1K", choices=["1K", "2K", "4K"])
    parser.add_argument("--output", required=True, help="Ziel-Pfad (.png)")
    parser.add_argument("--model", default="fal-ai/nano-banana-pro")
    parser.add_argument("--num-images", type=int, default=1)
    args = parser.parse_args()

    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        die('FAL_KEY fehlt. Setup: export FAL_KEY="<key-id>:<key-secret>" '
            "(Key erstellen: https://fal.ai/dashboard/keys)")

    headers = {"Authorization": f"Key {api_key}", "Content-Type": "application/json"}
    payload = {
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "num_images": args.num_images,
        "output_format": "png",
    }

    print(f"Generiere mit {args.model} ({args.aspect_ratio}, {args.resolution}) ...")
    result = request_json(f"https://queue.fal.run/{args.model}",
                          headers, data=json.dumps(payload).encode())

    if result.get("status") in ("IN_QUEUE", "IN_PROGRESS"):
        status_url = result.get("status_url")
        response_url = result.get("response_url")
        if not status_url or not response_url:
            die(f"Queue-Antwort ohne status_url/response_url: {json.dumps(result, indent=2)}")
        result = poll_for_result(status_url, response_url, headers)

    images = result.get("images") or result.get("output") or []
    if not images:
        die(f"Keine Bilder in der Antwort: {json.dumps(result, indent=2)}")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    for i, img in enumerate(images):
        url = img if isinstance(img, str) else img.get("url")
        if not url:
            die(f"Keine Bild-URL gefunden: {json.dumps(img, indent=2)}")
        target = output if len(images) == 1 else output.with_stem(f"{output.stem}-{i+1}")
        urllib.request.urlretrieve(url, str(target))
        print(f"Gespeichert: {target}  (URL: {url})")


if __name__ == "__main__":
    main()
