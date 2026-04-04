from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_mission_pdf(mission):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 14)

    p.drawString(50, 800, f"Mission: {mission.title}")
    p.drawString(50, 780, f"Client: {mission.client.email}")
    p.drawString(50, 760, f"Budget: {mission.budget}")
    p.drawString(50, 740, f"Deadline: {mission.deadline}")
    p.drawString(50, 720, f"Status: {mission.status}")

    p.drawString(50, 700, "Applications:")
    y = 680
    for app in mission.applications.all():
        p.drawString(60, y, f"{app.freelancer.email} → {app.status}")
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

