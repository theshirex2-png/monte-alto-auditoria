"""
Texto -> traco vetorial, com fontTools.

    python texto_para_traco.py

Converte um texto em <path> de SVG a partir de uma fonte do sistema, para o
lockup nao depender de fonte instalada em quem abre o arquivo.

Motivo: <text> no SVG usa a fonte que existir na maquina. Onde a fonte
faltar, o navegador usa uma substituta e o nome muda de forma e de largura.
Como path, o arquivo desenha exatamente o que esta gravado.

Fonte usada: Arial Bold (arialbd.ttf) para o nome forte, Arial (arial.ttf)
para o leve e para a assinatura. Sao metricamente parecidas, entao a linha
de base bate.
"""
from __future__ import annotations

from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.misc.transform import Transform
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ARIAL = Path(r"C:\Windows\Fonts\arial.ttf")
ARIAL_BD = Path(r"C:\Windows\Fonts\arialbd.ttf")

_cache: dict = {}


def _fonte(caminho: Path) -> TTFont:
    if caminho not in _cache:
        _cache[caminho] = TTFont(caminho)
    return _cache[caminho]


def texto_para_path(texto: str, fonte: Path, tamanho: float,
                    x: float, y: float, espaco: float = 0.0) -> tuple[str, float]:
    """Devolve (d, largura) do texto em coordenadas do viewBox.

    x e y sao a origem do primeiro glifo na linha de base.
    espaco e o entreletras, em px do viewBox (negativo aperta).

    Implementacao: cada glifo e desenhado em um SVGPathPen proprio, com a
    translacao ja somada ao offset acumulado do texto. Um TransformPen
    unico nao serve aqui: ele concatena os comandos de todos os glifos sem
    acumular a posicao horizontal, e "MONTE ALTO" saia com 42px de largura
    em vez de 405 — todas as letras sobrepostas na primeira coluna.

    A fonte tem y para cima, o SVG y para baixo. O espelho em y com origem
    na linha de base e o que leva coordenadas de fonte para o viewBox.
    """
    tt = _fonte(fonte)
    upem = tt["head"].unitsPerEm
    escala = tamanho / upem
    glifos = tt.getGlyphSet()
    cmap = tt.getBestCmap()

    partes: list[str] = []
    cursor = x
    for ch in texto:
        nome = cmap.get(ord(ch))
        if nome is None:
            cursor += tamanho * 0.5 + espaco
            continue
        pen = SVGPathPen(glifos)
        glifos[nome].draw(
            TransformPen(pen, Transform(escala, 0, 0, -escala, cursor, y)))
        cmd = pen.getCommands()
        if cmd:
            partes.append(cmd)
        cursor += glifos[nome].width * escala + espaco

    largura = cursor - x
    if espaco and texto:
        largura -= espaco  # o entreletras depois do ultimo nao conta
    return " ".join(partes), largura


def main() -> None:
    NEED = "MONTE ALTOAUDITORIAseguranca de codigo · auditoria de WordPress e PHP"
    for caminho, rotulo in [(ARIAL_BD, "Arial Bold"), (ARIAL, "Arial")]:
        if not caminho.exists():
            print(f"{rotulo}: fonte ausente em {caminho}")
            continue
        faltando = [c for c in sorted(set(NEED))
                    if ord(c) not in _fonte(caminho).getBestCmap()]
        print(f"{rotulo}: {len(set(NEED))} caracteres, faltando {faltando or 'nenhum'}")

    print()
    print("largura medida (viewBox de 1200):")
    for nome, fonte, tam, esp in [
        ("MONTE ALTO", ARIAL_BD, 62, -0.5),
        ("AUDITORIA", ARIAL, 62, 2.5),
        ("assinatura", ARIAL, 25, 0),
    ]:
        _, w = texto_para_path(nome, fonte, tam, 304, 176, esp)
        print(f"  {nome:<12} {tam}px esp={esp:<5} -> {w:>7.1f}px")


if __name__ == "__main__":
    main()