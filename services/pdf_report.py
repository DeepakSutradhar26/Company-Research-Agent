from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

from schema.form_submission import LeadInput
from schema.response import LeadResponse

def generate_pdf(lead: LeadInput, report: LeadResponse):
    try:
        os.makedirs('reports', exist_ok=True)
        filename = f"reports/{lead.company.replace(' ', '_')}_report.pdf"

        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        intel = report.intelligence
        audit = report.audit

        # Header
        story.append(Paragraph(f"{intel.company_name} - Intelligence Report", styles['Title']))
        story.append(Paragraph(f"Prepared for: {lead.name} | {lead.email}", styles['Normal']))
        story.append(Spacer(1, 12))

        # Company Info
        story.append(Paragraph("Company Overview", styles['Heading1']))
        story.append(Paragraph(f"Industry: {intel.industry or 'N/A'}", styles['Normal']))
        story.append(Paragraph(f"Founded: {intel.founded or 'N/A'}", styles['Normal']))
        story.append(Paragraph(f"Headquarters: {intel.headquarters or 'N/A'}", styles['Normal']))
        story.append(Paragraph(f"Size: {intel.company_size or 'N/A'}", styles['Normal']))
        story.append(Paragraph(intel.description or '', styles['Normal']))
        story.append(Spacer(1, 12))

        # Audit
        story.append(Paragraph("Executive Summary", styles['Heading1']))
        story.append(Paragraph(audit.executive_summary, styles['Normal']))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Strengths", styles['Heading1']))
        for s in audit.strengths:
            story.append(Paragraph(f"• {s}", styles['Normal']))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Potential Gaps", styles['Heading1']))
        for g in audit.potential_gaps:
            story.append(Paragraph(f"• {g}", styles['Normal']))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Recommended Solutions", styles['Heading1']))
        for r in audit.recommended_solutions:
            story.append(Paragraph(f"• {r}", styles['Normal']))

        doc.build(story)

        return {'success': True, 'path': filename}

    except Exception as e:
        return {'success': False, 'message': str(e)}