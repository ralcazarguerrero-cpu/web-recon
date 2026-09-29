import json
import os
from datetime import datetime


def save_report(target: str, data: dict, output_dir: str = "reports"):
    """Guarda el informe en JSON y en Markdown. Devuelve las rutas."""
    os.makedirs(output_dir, exist_ok=True)
    safe_target = target.replace("/", "_").replace(":", "_")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{output_dir}/{safe_target}_{ts}"

    json_path = f"{base}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    md_path = f"{base}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Informe de reconocimiento: {target}\n\n")
        f.write(f"Fecha: {datetime.now().isoformat()}\n\n")

        f.write("## Resolucion DNS\n")
        d = data.get("dns", {})
        f.write(f"- IP: {d.get('ip', 'N/A')}\n")
        f.write(f"- Reverse: {d.get('reverse', 'N/A')}\n\n")

        f.write("## Puertos abiertos\n")
        for p in data.get("ports", []):
            f.write(f"- {p['port']}/tcp - {p['service']}\n")
        f.write("\n")

        f.write("## Cabeceras HTTP\n")
        for h in data.get("http", []):
            f.write(f"### {h['url']}\n")
            f.write(f"- Status: {h.get('status')}\n")
            f.write(f"- Server: {h.get('server')}\n\n")

        f.write("## Rutas encontradas\n")
        for r in data.get("paths", []):
            f.write(f"- {r['path']} -> {r['status']} ({r['size']} bytes)\n")

    return json_path, md_path
