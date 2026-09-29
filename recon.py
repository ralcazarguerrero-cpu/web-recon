#!/usr/bin/env python3
"""
WebRecon - Script de reconocimiento web automatizado.
Lee el target desde .env y ejecuta DNS, puertos, HTTP y rutas comunes.
"""

import os
import sys
import logging
from dotenv import load_dotenv

from recon import dns, ports, http, report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


COMMON_PATHS = [
    "admin", "login", "robots.txt", "sitemap.xml", "backup",
    "wp-admin", "wp-login.php", "phpmyadmin", ".git/config",
    "config.php", "index.php", "api", "docs", "swagger",
    "server-status", ".env", "adminer.php",
]


def main():
    load_dotenv()

    target = os.getenv("TARGET", "").strip()
    if not target:
        logger.error("Falta TARGET en el archivo .env")
        sys.exit(1)

    ports_str = os.getenv("PORTS", "1-1000")
    timeout = float(os.getenv("TIMEOUT", "2"))
    threads = int(os.getenv("THREADS", "100"))

    logger.info(f"Target: {target}")

    data = {"target": target}

    # 1. DNS
    logger.info("Resolviendo DNS...")
    dns_result = dns.resolve(target)
    data["dns"] = dns_result
    if dns_result["ip"]:
        logger.info(f"  IP: {dns_result['ip']}")

    # 2. Puertos
    logger.info("Escaneando puertos...")
    port_list = ports.parse_ports(ports_str)
    open_ports = ports.scan(target, port_list, timeout=timeout, threads=threads)
    data["ports"] = open_ports
    logger.info(f"  {len(open_ports)} puertos abiertos")

    # 3. HTTP
    data["http"] = []
    data["paths"] = []
    http_ports = [p["port"] for p in open_ports if p["port"] in (80, 443, 8080, 8443)]
    for p in http_ports:
        scheme = "https" if p in (443, 8443) else "http"
        url = f"{scheme}://{target}" + (f":{p}" if p not in (80, 443) else "")
        logger.info(f"Analizando {url}...")
        h = http.grab_headers(url)
        data["http"].append(h)

        paths_found = http.check_paths(url, COMMON_PATHS)
        data["paths"].extend([{**p, "url": url} for p in paths_found])

    # 4. Informe
    logger.info("Generando informe...")
    json_path, md_path = report.save_report(target, data)
    logger.info(f"Informe JSON: {json_path}")
    logger.info(f"Informe Markdown: {md_path}")


if __name__ == "__main__":
    main()
