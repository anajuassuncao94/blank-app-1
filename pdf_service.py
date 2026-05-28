from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def gerar_pdf_cronograma(usuario: dict, cronograma: dict, itens: list[dict]) -> bytes:
    """Gera PDF do cronograma semanal."""
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("OrganizaAí Estudos", styles["Title"]))
    story.append(Paragraph("Cronograma Semanal de Estudos", styles["Heading2"]))
    story.append(Paragraph(f"Usuário: {usuario['nome']}", styles["Normal"]))
    story.append(Paragraph(f"Gerado em: {cronograma['data_criacao']}", styles["Normal"]))
    story.append(Spacer(1, 0.4 * cm))

    dados = [["Dia", "Início", "Fim", "Atividade"]]
    for item in itens:
        dados.append(
            [
                item["dia_semana"],
                str(item["hora_inicio"])[:5],
                str(item["hora_fim"])[:5],
                item["descricao"],
            ]
        )

    tabela = Table(dados, colWidths=[3 * cm, 2.2 * cm, 2.2 * cm, 17 * cm])
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ]
        )
    )

    story.append(tabela)
    doc.build(story)

    buffer.seek(0)
    return buffer.read()
