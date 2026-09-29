import socket
import logging

logger = logging.getLogger(__name__)


def resolve(target: str) -> dict:
    """Resuelve un dominio a IP y hace reverse lookup."""
    result = {"target": target, "ip": None, "reverse": None, "error": None}
    try:
        ip = socket.gethostbyname(target)
        result["ip"] = ip
        try:
            reverse = socket.gethostbyaddr(ip)[0]
            result["reverse"] = reverse
        except Exception:
            pass
    except Exception as e:
        result["error"] = str(e)
        logger.warning(f"DNS fallo para {target}: {e}")
    return result
