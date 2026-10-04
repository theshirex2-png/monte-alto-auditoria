"""
Le sites publicos e identifica sinal de WordPress + dado de contato.

So LEITURA de pagina publica. Nao envia nada, nao contata ninguem.
Escreve saida em JSON para o CRM.

    python prospectar.py --saida prospects.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx

# Agente honesto: identifica-se e nao finge ser buscador.
UA = "Mozilla/5.0 (compatible; auditoria-tecnica/1.0; +contato-local)"

RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-z]{2,}", re.I)
RE_WHATS = re.compile(r"whatsapp\.com/send\?phone=(\d{10,15})", re.I)
RE_WHATS_BR = re.compile(r"(?:wa\.me|api\.whatsapp\.com/send\?phone=)(\d{10,15})", re.I)
RE_TEL = re.compile(r"href=[\"\'](?:tel:|https?://wa\.me/)\+?(\d{10,15})", re.I)

# Sinais de WordPress, e o que cada um indica.
SINAIS_WP = {
    "wp-content": "WordPress",
    "wp-includes": "WordPress",
    "/wp-json/": "WordPress REST API",
    "wp-content/plugins/elementor": "Elementor",
    "wp-content/plugins/contact-form": "plugin de formulário",
    "wp-content/themes/": "tema WordPress",
}

# Caminho onde a área administrativa responde 200 em WP.
CAMINHOS_ADMIN = ["/wp-admin/", "/wp-login.php"]


def ver_site(url: str, cliente: httpx.Client) -> dict:
    """Busca o site e devolve o que der para extrair publicamente."""
    r = {"url": url, "ok": False, "wp": [], "email": [], "whatsapp": [],
         "telefone": [], "erro": "", "titulo": ""}

    try:
        resp = cliente.get(url, timeout=25, follow_redirects=True)
        if resp.status_code >= 400:
            r["erro"] = f"HTTP {resp.status_code}"
            return r
        html = resp.text.lower()
        r["ok"] = True
        r["titulo"] = re.search(r"<title[^>]*>([^<]{0,120})", resp.text, re.I)
        r["titulo"] = r["titulo"].group(1).strip() if r["titulo"] else ""
        r["final_url"] = str(resp.url)

        for sinal, nome in SINAIS_WP.items():
            if sinal in html:
                r["wp"].append(nome)

        r["email"] = sorted(set(RE_EMAIL.findall(resp.text)))
        r["whatsapp"] = sorted(set(
            RE_WHATS.findall(resp.text) + RE_WHATS_BR.findall(resp.text)
        ))
        r["telefone"] = sorted(set(RE_TEL.findall(resp.text)))

        base = urljoin(str(resp.url), "/")
        for cam in CAMINHOS_ADMIN:
            try:
                h = cliente.get(urljoin(base, cam.lstrip("/")),
                                timeout=12, follow_redirects=True)
                if h.status_code < 400:
                    r.setdefault("admin_responde", []).append(cam)
            except httpx.HTTPError:
                pass

    except httpx.HTTPError as e:
        r["erro"] = f"{type(e).__name__}: {e}"
    except Exception as e:  # noqa: BLE001
        r["erro"] = f"{type(e).__name__}: {e}"

    return r


def score(r: dict) -> int:
    """Quanto maior, mais provável contratar auditoria."""
    if not r.get("ok"):
        return -100
    p = 0
    # Ter WordPress é o requisito mínimo do serviço.
    if any("WordPress" in x for x in r.get("wp", [])):
        p += 30
    # Tema e plugin são onde mora o problema.
    if any("tema" in x for x in r.get("wp", [])):
        p += 5
    if any("plugin" in x for x in r.get("wp", [])):
        p += 5
    if "Elementor" in r.get("wp", []):
        p += 5
    # Admin exposto é o achado mais vendável que existe.
    if r.get("admin_responde"):
        p += 25
    # Contato direto é o que permite responder.
    if r.get("email"):
        p += 10
    if r.get("whatsapp"):
        p += 15
    if r.get("telefone"):
        p += 5
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alvos", help="arquivo txt com um site por linha")
    ap.add_argument("--saida", default="prospects.json")
    args = ap.parse_args()

    if not args.alvos:
        print(__doc__)
        return 1

    alvos = [l.strip() for l in
             Path(args.alvos).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]

    with httpx.Client(headers={"User-Agent": UA}, timeout=25,
                      follow_redirects=True) as cliente:
        resultados = []
        with ThreadPoolExecutor(max_workers=6) as pool:
            futuros = {pool.submit(ver_site, a, cliente): a for a in alvos}
            for fut in as_completed(futuros):
                r = fut.result()
                r["score"] = score(r)
                resultados.append(r)
                marca = "OK " if r["score"] > 0 else "-- "
                print(f"{marca}{r['score']:>4}  {r['url']}  {', '.join(r['wp'][:3])}")

    resultados.sort(key=lambda x: x["score"], reverse=True)
    saida = Path(args.saida)
    saida.write_text(json.dumps(resultados, ensure_ascii=False, indent=2),
                     encoding="utf-8")
    print(f"\n{len(resultados)} site(s) em {saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())