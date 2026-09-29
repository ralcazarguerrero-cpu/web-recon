import requests
import logging

logger = logging.getLogger(__name__)


def grab_headers(url: str, timeout: float = 5) -> dict:
    """Coge las cabeceras HTTP de una URL."""
    result = {"url": url, "status": None, "server": None, "headers": {}, "error": None}
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True)
        result["status"] = r.status_code
        result["headers"] = dict(r.headers)
        result["server"] = r.headers.get("Server", "no declarado")
    except Exception as e:
        result["error"] = str(e)
        logger.warning(f"HTTP fallo para {url}: {e}")
    return result


def check_paths(base_url: str, paths: list, timeout: float = 5) -> list:
    """Comprueba rutas comunes y devuelve las que responden != 404."""
    found = []
    for path in paths:
        url = base_url.rstrip("/") + "/" + path.lstrip("/")
        try:
            r = requests.get(url, timeout=timeout, allow_redirects=False)
            if r.status_code != 404:
                found.append({"path": path, "status": r.status_code, "size": len(r.content)})
                logger.info(f"  {path} -> {r.status_code}")
        except Exception:
            pass
    return found
