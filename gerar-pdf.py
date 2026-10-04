"""
Gera o relatório de auditoria em PDF a partir do JSON do auditoria_remota.py.

    python gerar-pdf.py auditoria_cliente.json
    python gerar-pdf.py auditoria_cliente.json --saida relatório.pdf

Depende de reportlab. Se não tiver:
    pip install reportlab
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        HRFlowable,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError:
    print("Falta o reportlab. Instale com:  pip install reportlab")
    raise SystemExit(1)

VERDE = colors.HexColor("#1a7f37")
VERMELHO = colors.HexColor("#cf222e")
AMARELO = colors.HexColor("#bf8700")
CINZA = colors.HexColor("#57606a")
CINZA_CLARO = colors.HexColor("#f6f8fa")
BORDA = colors.HexColor("#d0d7de")

SEVERIDADE = {
    "critica": VERMELHO,
    "alta": VERMELHO,
    "media": AMARELO,
    "baixa": colors.HexColor("#1f6feb"),
    "manutencao": CINZA,
}


def estilo():
    base = getSampleStyleSheet()
    s = {}
    s["titulo"] = ParagraphStyle(
        "titulo", parent=base["Title"], fontSize=22, textColor=VERDE,
        spaceAfter=4, fontName="Helvetica-Bold",
    )
    s["sub"] = ParagraphStyle(
        "sub", parent=base["Normal"], fontSize=10, textColor=CINZA,
        spaceAfter=18,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Heading2"], fontSize=14, textColor=colors.black,
        spaceBefore=16, spaceAfter=8, fontName="Helvetica-Bold",
    )
    s["achado"] = ParagraphStyle(
        "achado", parent=base["Normal"], fontSize=11, spaceAfter=3,
        fontName="Helvetica-Bold",
    )
    s["corpo"] = ParagraphStyle(
        "corpo", parent=base["Normal"], fontSize=9.5, spaceAfter=2,
    )
    s["mono"] = ParagraphStyle(
        "mono", parent=base["Normal"], fontSize=8.5, fontName="Courier",
        textColor=CINZA, spaceAfter=6,
    )
    s["pe"] = ParagraphStyle(
        "pe", parent=base["Normal"], fontSize=8, textColor=CINZA,
        alignment=1,
    )
    return s


def carregar(caminho: Path) -> dict:
    d = json.loads(caminho.read_text(encoding="utf-8"))
    if isinstance(d, list):
        return {"achados": d}
    return d


def gerar(entrada: Path, saida: Path) -> Path:
    dados = carregar(entrada)
    cliente = dados.get("cliente") or entrada.stem.replace("_", " ")
    achados = dados.get("achados") or dados.get("achados_por_categoria") or []
    if isinstance(achados, dict):
        achados = [a for lista in achados.values() for a in (lista or [])]
    s = estilo()

    doc = SimpleDocTemplate(
        str(saida), pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=f"Auditoria de código — {cliente}",
        author="Monte Alto Auditoria",
    )

    hist = []

    def cabecalho(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(CINZA)
        canvas.drawString(2.2 * cm, A4[1] - 1.2 * cm,
                          "Monte Alto Auditoria  ·  Serra e Vila Velha, ES")
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.3 * cm, str(doc.page))
        canvas.setStrokeColor(BORDA)
        canvas.setLineWidth(0.4)
        canvas.line(2.2 * cm, A4[1] - 1.5 * cm, A4[0] - 2.2 * cm, A4[1] - 1.5 * cm)
        canvas.restoreState()

    hist.append(Paragraph("Auditoria de código", s["titulo"]))
    hist.append(Paragraph(
        f"<b>{cliente}</b> &nbsp;·&nbsp; {date.today().strftime('%d/%m/%Y')}",
        s["sub"]))

    # ---- resumo
    contagem = {}
    for a in achados:
        sev = str(a.get("critica", a.get("severidade", "media"))).lower()
        contagem[sev] = contagem.get(sev, 0) + 1

    resumo = [["Severidade", "Quantidade"]]
    for sev in ("critica", "alta", "media", "baixa", "manutencao"):
        if contagem.get(sev):
            resumo.append([sev.capitalize(), str(contagem[sev])])
    if not contagem:
        resumo = [["Nenhum achado", "0"]]
    resumo.append(["Total", str(len(achados))])

    t = Table(resumo, colWidths=[6 * cm, 4 * cm], hAlign="LEFT")
    estilo_t = [
        ("BACKGROUND", (0, 0), (-1, 0), CINZA_CLARO),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDA),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i, sev in enumerate(("critica", "alta", "media", "baixa", "manutencao"), start=1):
        if contagem.get(sev):
            estilo_t.append(("TEXTCOLOR", (0, i), (0, i), SEVERIDADE.get(sev, CINZA)))
    estilo_t.append(("FONTNAME", (0, len(resumo) - 1), (-1, len(resumo) - 1), "Helvetica-Bold"))
    t.setStyle(TableStyle(estilo_t))

    hist.append(Paragraph("Resumo", s["h2"]))
    hist.append(t)
    hist.append(Spacer(1, 10))
    hist.append(Paragraph(
        "Este relatório cobre exposição de erro, versão de dependências, "
        "padrões inseguros no código e pontos de lentidão. O diagnóstico "
        "não inclui correção: correção é orcada a parte.", s["corpo"]))

    # ---- achados
    hist.append(Paragraph("Achados", s["h2"]))
    if not achados:
        hist.append(Paragraph(
            "Nenhum problema critico ou alto foi encontrado. O site esta "
            "dentro do aceitavel nas categorias auditadas.", s["corpo"]))
    else:
        for i, a in enumerate(achados, start=1):
            sev = str(a.get("critica", a.get("severidade", "media"))).lower()
            cor = SEVERIDADE.get(sev, CINZA)
            hist.append(Paragraph(
                f'<font color="{cor.hexval()}">■</font> '
                f"{i}. {a.get('nome', a.get('titulo', 'Achado'))}",
                s["achado"]))
            onde = a.get("arquivo") or a.get("caminho") or ""
            linhas = a.get("linhas") or a.get("linha")
            if onde:
                hist.append(Paragraph(
                    f"{onde}" + (f":{linhas}" if linhas else ""), s["mono"]))
            if a.get("descricao"):
                hist.append(Paragraph(a["descricao"], s["corpo"]))
            if a.get("correcao"):
                hist.append(Paragraph(
                    f"<b>Correção sugerida:</b> {a['correcao']}", s["corpo"]))
            hist.append(Spacer(1, 10))

    hist.append(Spacer(1, 18))
    hist.append(HRFlowable(width="100%", color=BORDA))
    hist.append(Spacer(1, 8))
    hist.append(Paragraph(
        "Monte Alto Auditoria &nbsp;·&nbsp; 27 99818-5280 &nbsp;·&nbsp; "
        "Serra e Vila Velha, ES &nbsp;·&nbsp; Correcao: R$ 90/hora", s["pe"]))

    doc.build(hist, onFirstPage=cabecalho, onLaterPages=cabecalho)
    return saida


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada", help="JSON gerado pelo auditoria_remota.py")
    ap.add_argument("--saida", help="PDF de saida")
    args = ap.parse_args()

    ent = Path(args.entrada)
    if not ent.exists():
        print(f"não achei: {ent}")
        raise SystemExit(1)

    saida = Path(args.saida) if args.saida else ent.with_suffix(".pdf")
    p = gerar(ent, saida)
    print(f"gerado: {p}")
    print(f"tamanho: {p.stat().st_size} bytes")