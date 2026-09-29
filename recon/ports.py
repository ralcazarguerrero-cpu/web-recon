import socket
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
    6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB",
}


def parse_ports(ports_str: str) -> list:
    """Parsea '1-1000' o '22,80,443' a lista de enteros."""
    ports = []
    for part in ports_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return ports


def _check_port(target: str, port: int, timeout: float):
    """Intenta conectar a un puerto. Devuelve el puerto si esta abierto."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((target, port)) == 0:
                return port
    except Exception:
        pass
    return None


def scan(target: str, ports: list, timeout: float = 2, threads: int = 100) -> list:
    """Escanea una lista de puertos en paralelo."""
    open_ports = []
    logger.info(f"Escaneando {len(ports)} puertos en {target}...")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(_check_port, target, p, timeout): p for p in ports}
        for future in as_completed(futures):
            port = future.result()
            if port:
                service = COMMON_SERVICES.get(port, "desconocido")
                open_ports.append({"port": port, "service": service})
                logger.info(f"  Puerto {port} abierto ({service})")

    return sorted(open_ports, key=lambda x: x["port"])
