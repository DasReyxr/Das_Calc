
"""Consulta de versión en GitHub Releases y reemplazo del ejecutable (sin tkinter)."""
import json
import os
import re
import subprocess
import sys
import urllib.request

import shutil
import tarfile

from .version import __version__

REPO = "DasReyxr/Das_Calc"  # confirma owner/repo
API = f"https://api.github.com/repos/{REPO}/releases/latest"


def _asset_name():
    if sys.platform == "win32":
        return "DasCalculator-windows.exe"
    if sys.platform == "darwin":
        return "DasCalculator-macos.tar.gz"
    return "DasCalculator-linux"  # binario directo, sin tar

def _parse(v: str):
    return tuple(int(n) for n in re.findall(r"\d+", v))


def check_latest():
    """Devuelve dict con version/asset_url/page si hay una versión más nueva; si no, None."""
    req = urllib.request.Request(API, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=8) as r:
        data = json.load(r)
    tag = data["tag_name"]
    if _parse(tag) <= _parse(__version__):
        return None
    asset = next((a for a in data["assets"] if a["name"] == _asset_name()), None)
    return {
        "version": tag.lstrip("vV"),
        "asset_url": asset["browser_download_url"] if asset else None,
        "page": data["html_url"],
    }


def can_self_update() -> bool:
    return getattr(sys, "frozen", False)  # solo el ejecutable empaquetado


def download_and_replace(asset_url: str):
    exe = sys.executable
    new, tmp = exe + ".new", exe + ".download"
    urllib.request.urlretrieve(asset_url, tmp)
    if asset_url.endswith(".tar.gz"):          # macOS
        with tarfile.open(tmp) as t, open(new, "wb") as out:
            shutil.copyfileobj(t.extractfile("DasCalculator"), out)
        os.remove(tmp)
    else:
        os.replace(tmp, new)
    os.chmod(new, 0o755)
    if sys.platform == "win32":
        old = exe + ".old"
        if os.path.exists(old):
            os.remove(old)
        os.rename(exe, old)
        os.rename(new, exe)
    else:
        os.replace(new, exe)
    subprocess.Popen([exe])
    os._exit(0)