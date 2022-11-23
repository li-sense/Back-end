from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas 


class CriacaoDoCertificado():
    def createPDF():
        A4 = (297*mm, 210*mm)

        cnv = canvas.Canvas("meu_pdf.pdf") 

        cnv.setPageSize(A4)

        cnv.setFont('Helvetica-Bold', 38)
        cnv.drawString(100, 430, "Certificado de Compra da licença")

        cnv.drawImage("./app/asset/images/logoFinal.png", 50, 500, width=150, height=50)

        cnv.rect(30, 30, 780, 540)

        cnv.setFont('Helvetica', 26 )
        cnv.drawString(80, 300, "A empresa Li-Sense afirma por meio deste documento que o")
        cnv.drawString(80, 270,  "usuário(a)tem direito de posse da licença desse produto.")

        pdf = cnv.save()
        return pdf