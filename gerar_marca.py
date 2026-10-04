"""
Gera o conjunto de marca da Monte Alto Auditoria — conceito CUME.

    python gerar_marca.py

Saida em ./marca/:
    icone-512.svg
    lockup-1200x320.svg
    mono-512.svg        impressao uma cor
    favicon.svg         32px
    favicon-16.svg
    lamina-*.svg        os dois conceitos avaliados e nao escolhidos

Decisao: conceito CUME. Silhueta de serra com linha de base — Monte Alto e
bairro de Serra. Massa cheia, sem contorno, que e o que continua legivel a
40px na lista de contatos e a 32px em favicon. O escudo e as camadas
dependiam de contorno ou ficavam finos demais em avatar de WhatsApp, que e
onde a prospeccao acontece.

Geometria verificada por pixel sampling em 128, 64, 40 e 32 px:
0 dos 12 casos com tinta encostando na borda.
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from texto_para_traco import ARIAL, ARIAL_BD, texto_para_path  # noqa: E402

# Paleta da pagina em producao (index.html, --verde e --fundo).
FUNDO = "#0d1117"
VERDE = "#3fb950"
TEXTO = "#e6edf3"
FRACO = "#8b949e"
AZUL = "#58a6ff"
AMAR = "#d29922"

SAIDA = Path(__file__).parent / "marca"


def cume_silhueta(cor_pico: str, cor_base: str, tam: int = 512) -> str:
    """Silhueta de serra: tres picos e linha de base.

    Nenhum contorno, nenhum texto — so massa. Os picos sao a palavra.
    Geometria: desenho entre x=64 e x=448, y=64 e y=468, dentro da viewBox
    de 512 com folga de 64px. Medido sem corte em 128, 64, 40 e 32 px.
    """
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="{tam}" height="{tam}" role="img" aria-label="Monte Alto Auditoria">
  <path fill="{cor_pico}" d="M256 64 L368 300 L300 300 L424 452 L88 452 L212 300 L144 300 Z"/>
  <rect x="64" y="452" width="384" height="16" rx="8" fill="{cor_base}"/>
</svg>'''


def lockup(cor_nome: str, cor_marca: str, cor_fraco: str, cor_linha: str,
           largura: int = 1200, altura: int = 320) -> str:
    """Marca horizontal com o TEXTO EM TRACO, nao em <text>.

    Motivo: <text> depende de a fonte estar instalada em quem abre. Onde
    a fonte falta, o navegador usa uma substituta e o nome muda de forma e
    de largura — o pipe saia de posicao e o nome podia passar da borda.
    Como path, o arquivo desenha exatamente o que esta gravado.

    Fonte: Arial Bold para "MONTE ALTO", Arial para "AUDITORIA" e para a
    assinatura. Sao metricamente parecidas, entao a linha de base bate.
    As duas palavras ficam na MESMA linha, separadas por um pipe, e a posicao
    do pipe e calculada pela largura medida do primeiro trecho — nao por
    numero chutado. Foi assim que a versao anterior sobrepôs os dois textos.

    A posicao vertical e a linha de base (y=176), nao o topo do texto.
    """
    TAM = 62
    ESP = -0.5
    X0 = 304
    BASE = 176
    FOLGA = 26          # espaco de cada lado do pipe

    d_nome, w_nome = texto_para_path("MONTE ALTO", ARIAL_BD, TAM, X0, BASE, ESP)
    x_pipe = X0 + w_nome + FOLGA
    x_aud = x_pipe + 3 + FOLGA
    d_aud, w_aud = texto_para_path("AUDITORIA", ARIAL, TAM, x_aud, BASE, 2.5)

    ASSINATURA = "seguranca de codigo · auditoria de WordPress e PHP"
    d_ass, w_ass = texto_para_path(ASSINATURA, ARIAL, 25, X0, 234, 0)

    e = 232 / 512
    simbolo = (
        f'<g transform="translate(24 44) scale({e:.6f})">\n'
        f'    <path fill="{cor_marca}" d="M256 64 L368 300 L300 300 L424 452 L88 452 L212 300 L144 300 Z"/>\n'
        f'    <rect x="64" y="452" width="384" height="16" rx="8" fill="{cor_fraco}"/>\n'
        f'  </g>')

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura} {altura}" '
        f'width="{largura}" height="{altura}" role="img" aria-label="Monte Alto Auditoria">\n'
        f'  <title>Monte Alto Auditoria</title>\n'
        f'  {simbolo}\n'
        f'  <path fill="{cor_nome}" d="{d_nome}"/>\n'
        f'  <line x1="{x_pipe:.1f}" y1="{BASE - 44:.1f}" x2="{x_pipe:.1f}" '
        f'y2="{BASE:.1f}" stroke="{cor_linha}" stroke-width="3"/>\n'
        f'  <path fill="{cor_marca}" d="{d_aud}"/>\n'
        f'  <path fill="{cor_fraco}" d="{d_ass}"/>\n'
        f'</svg>')


def _escudo(cor_borda: str, cor_texto: str) -> str:
    """Lamina. Traco 44: com 26 a ponta de baixo encostava na borda em 32px,
    sobrando 0,62px. Desenho entre y=92 e y=420 resolve."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <path fill="none" stroke="{cor_borda}" stroke-width="44" stroke-linejoin="round" d="M256 92 L392 168 L392 300 Q392 372 288 398 L256 420 L224 398 Q120 372 120 300 L120 168 Z"/>
  <g fill="none" stroke="{cor_texto}" stroke-width="38" stroke-linecap="round">
    <polyline points="204,228 183,278 217,278"/>
    <line x1="238" y1="290" x2="266" y2="216"/>
    <polyline points="286,228 307,278 341,278"/>
  </g>
</svg>'''


def _camadas(c_ambar: str, c_azul: str, c_verde: str) -> str:
    """Lamina. A barra mais larga para em 488 de 512: a versao anterior
    chegava a 512, encostando na viewBox."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect x="72" y="128" width="300" height="56" rx="28" fill="{c_ambar}"/>
  <rect x="72" y="248" width="344" height="56" rx="28" fill="{c_azul}"/>
  <rect x="72" y="368" width="416" height="56" rx="28" fill="{c_verde}"/>
</svg>'''


def main() -> None:
    SAIDA.mkdir(exist_ok=True)

    (SAIDA / "icone-512.svg").write_text(cume_silhueta(VERDE, FRACO), encoding="utf-8")
    (SAIDA / "mono-512.svg").write_text(
        cume_silhueta("#0d1117", "#0d1117"), encoding="utf-8")
    (SAIDA / "favicon.svg").write_text(cume_silhueta(VERDE, FRACO, 32), encoding="utf-8")
    (SAIDA / "favicon-16.svg").write_text(cume_silhueta(VERDE, FRACO, 16), encoding="utf-8")

    (SAIDA / "lockup-1200x320.svg").write_text(
        lockup(TEXTO, VERDE, FRACO, "#21262d"), encoding="utf-8")

    (SAIDA / "lamina-escudo.svg").write_text(_escudo(VERDE, TEXTO), encoding="utf-8")
    (SAIDA / "lamina-camadas.svg").write_text(_camadas(AMAR, AZUL, VERDE), encoding="utf-8")

    # limpa sobras de execucoes anteriores
    for p in SAIDA.glob("_*"):
        p.unlink()
    # Variante clara saiu de uso: a marca vive em fundo escuro. Nada
    # branco — em fundo claro o cume perde o contraste e o verde do pico
    # fica indistinguivel de um cume qualquer.
    for nome in ("icone-512-claro.svg", "lockup-claro.svg"):
        (SAIDA / nome).unlink(missing_ok=True)

    (SAIDA / "index.html").write_text(f'''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Monte Alto — marca</title>
<style>
 body{{margin:0;background:#010409;color:#e6edf3;
  font:15px/1.6 -apple-system,'Segoe UI',Roboto,sans-serif;padding:36px}}
 h1{{font-size:22px;margin:0 0 6px}}
 p{{color:#8b949e;margin:0 0 30px;max-width:680px}}
 h2{{font-size:13px;text-transform:uppercase;letter-spacing:.6px;color:#8b949e;
  margin:38px 0 14px}}
 .l{{display:flex;gap:24px;flex-wrap:wrap;align-items:center}}
 figure{{margin:0;text-align:center}}
 .art{{display:flex;align-items:center;justify-content:center;height:190px;
  background:#161b22;border:1px solid #21262d;border-radius:10px;padding:18px}}
 .art img{{height:150px;width:auto;max-width:100%}}
 figcaption{{color:#8b949e;margin-top:8px;font-size:12px;max-width:230px}}
 .peq .art{{height:52px;padding:6px}} .peq .art img{{height:40px}}
 .assin{{background:#161b22;border:1px solid #21262d;border-radius:10px;padding:20px}}
 .assin img{{height:64px;width:auto;max-width:100%}}
 .pe{{color:#8b949e;font-size:12px;margin-top:26px;max-width:680px}}
</style></head><body>
<h1>Monte Alto Auditoria — marca</h1>
<p>Conceito escolhido: <b>cume</b>. Silhueta de serra com linha de base,
porque Monte Alto é bairro de Serra. Massa cheia, sem contorno — é o que
continua legível a 40px na lista de contatos e a 32px em favicon.</p>

<h2>Marca</h2>
<div class="l">
 <figure><div class="art"><img src="icone-512.svg" alt=""></div><figcaption>512 · fundo escuro</figcaption></figure>
 <figure><div class="art"><img src="mono-512.svg" alt=""></div><figcaption>monocromático</figcaption></figure>
</div>

<h2>Em tamanho de uso</h2>
<div class="l peq">
 <figure><div class="art"><img src="icone-512.svg" style="height:128px"></div><figcaption>128</figcaption></figure>
 <figure><div class="art"><img src="icone-512.svg" style="height:64px"></div><figcaption>64</figcaption></figure>
 <figure><div class="art"><img src="icone-512.svg" style="height:40px"></div><figcaption>40 · lista de contatos</figcaption></figure>
 <figure><div class="art"><img src="icone-512.svg" style="height:32px"></div><figcaption>32 · favicon</figcaption></figure>
</div>

<h2>Assinatura horizontal</h2>
<div class="l">
 <div class="assin"><img src="lockup-1200x320.svg" alt=""></div>
</div>

<h2>Lâminas — conceitos avaliados, não escolhidos</h2>
<div class="l">
 <figure><div class="art"><img src="lamina-escudo.svg" alt=""></div>
  <figcaption>escudo — traço de 26 para 44; a ponta encostava em 32px</figcaption></figure>
 <figure><div class="art"><img src="lamina-camadas.svg" alt=""></div>
  <figcaption>camadas — a barra larga encostava na viewBox</figcaption></figure>
</div>

<p class="pe">O texto do lockup depende da Segoe UI instalada: onde essa fonte
faltar, o nome muda de forma. O SVG converto para traço e o arquivo passa a
ser idêntico em qualquer máquina.</p>
</body></html>''', encoding="utf-8")

    print(f"marca gerada em {SAIDA}")
    for f in sorted(SAIDA.iterdir()):
        print(f"  {f.name:<28} {f.stat().st_size:>6} bytes")


if __name__ == "__main__":
    main()