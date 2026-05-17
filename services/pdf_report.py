import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable

from schema.form_submission import LeadInput
from schema.response import LeadResponse

# ── Brand Palette ──────────────────────────────────────────────────────────────
DARK_BG      = colors.HexColor('#0A0F1E')
ACCENT       = colors.HexColor('#4F8EF7')
ACCENT2      = colors.HexColor('#7C3AED')
ACCENT_LIGHT = colors.HexColor('#EEF3FF')
TEXT_MAIN    = colors.HexColor('#1A1F36')
TEXT_SUB     = colors.HexColor('#5A6478')
WHITE        = colors.white
GREEN        = colors.HexColor('#10B981')
AMBER        = colors.HexColor('#F59E0B')
RED_SOFT     = colors.HexColor('#EF4444')

PAGE_W, PAGE_H = A4
L_MARGIN = 14 * mm
R_MARGIN = 14 * mm
T_MARGIN = 18 * mm
B_MARGIN = 16 * mm
CONTENT_W = PAGE_W - L_MARGIN - R_MARGIN


# ── Canvas decorator ───────────────────────────────────────────────────────────
class HeaderFooterCanvas(canvas.Canvas):
    def __init__(self, *args, company_name='', **kwargs):
        super().__init__(*args, **kwargs)
        self.company_name = company_name
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_header_footer(total)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _draw_header_footer(self, total_pages):
        self.saveState()
        w, h = PAGE_W, PAGE_H

        # Top bar
        self.setFillColor(DARK_BG)
        self.rect(0, h - 14*mm, w, 14*mm, fill=1, stroke=0)
        self.setFillColor(WHITE)
        self.setFont('Helvetica-Bold', 9)
        self.drawString(14*mm, h - 9*mm, 'SimplifIQ')
        self.setFillColor(ACCENT)
        self.drawString(14*mm + 46, h - 9*mm, '·')
        self.setFillColor(colors.HexColor('#A0AEC0'))
        self.setFont('Helvetica', 8)
        self.drawString(14*mm + 56, h - 9*mm, 'AI Intelligence Report')
        self.setFillColor(WHITE)
        self.setFont('Helvetica-Bold', 8)
        self.drawRightString(w - 14*mm, h - 9*mm, self.company_name[:40])

        # Bottom bar
        self.setFillColor(DARK_BG)
        self.rect(0, 0, w, 10*mm, fill=1, stroke=0)
        self.setStrokeColor(ACCENT)
        self.setLineWidth(0.5)
        self.line(0, 10*mm, w, 10*mm)
        self.setFillColor(colors.HexColor('#A0AEC0'))
        self.setFont('Helvetica', 7)
        self.drawString(14*mm, 3.5*mm,
            f'Confidential · Generated {datetime.now().strftime("%B %d, %Y")}')
        self.drawRightString(w - 14*mm, 3.5*mm,
            f'Page {self._pageNumber} of {total_pages}')

        self.restoreState()


# ── Cover page ─────────────────────────────────────────────────────────────────
class CoverPage(Flowable):
    def __init__(self, company_name, lead_name, lead_email, industry, date_str):
        super().__init__()
        self.company_name = company_name
        self.lead_name    = lead_name
        self.lead_email   = lead_email
        self.industry     = industry or 'Technology'
        self.date_str     = date_str

    def wrap(self, availW, availH):
        return availW, availH

    def draw(self):
        c = self.canv
        c.translate(-L_MARGIN, -B_MARGIN)   # escape doc margins → full page
        w, h = PAGE_W, PAGE_H

        c.setFillColor(DARK_BG)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Diagonal accent top-right
        p = c.beginPath()
        p.moveTo(w * 0.55, h); p.lineTo(w, h); p.lineTo(w, h * 0.55); p.close()
        c.setFillColor(colors.HexColor('#1A0A3E'))
        c.drawPath(p, fill=1, stroke=0)

        p2 = c.beginPath()
        p2.moveTo(w * 0.75, h); p2.lineTo(w, h); p2.lineTo(w, h * 0.78); p2.close()
        c.setFillColor(colors.HexColor('#0D1F4A'))
        c.drawPath(p2, fill=1, stroke=0)

        # Accent line + label
        c.setStrokeColor(ACCENT); c.setLineWidth(2)
        c.line(14*mm, h * 0.72, 80*mm, h * 0.72)
        c.setFillColor(ACCENT); c.setFont('Helvetica-Bold', 8)
        c.drawString(14*mm, h * 0.74, 'COMPANY INTELLIGENCE REPORT')

        # Company name
        c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 32)
        name = self.company_name
        if len(name) > 22:
            sp = name.rfind(' ', 0, len(name)//2 + 5)
            if sp > 0:
                c.drawString(14*mm, h * 0.65, name[:sp])
                c.setFont('Helvetica-Bold', 28)
                c.drawString(14*mm, h * 0.59, name[sp+1:])
            else:
                c.setFont('Helvetica-Bold', 22)
                c.drawString(14*mm, h * 0.64, name)
        else:
            c.drawString(14*mm, h * 0.64, name)

        # Industry pill
        px, py = 14*mm, h * 0.53
        pw = len(self.industry) * 5.5 + 16
        c.setFillColor(ACCENT)
        c.roundRect(px, py, pw, 7*mm, 3.5*mm, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 8)
        c.drawString(px + 8, py + 2.3*mm, self.industry.upper())

        # Divider
        c.setStrokeColor(colors.HexColor('#2A3A5C')); c.setLineWidth(0.5)
        c.line(14*mm, h * 0.49, w - 14*mm, h * 0.49)

        # Prepared for
        c.setFillColor(colors.HexColor('#7A8AAA')); c.setFont('Helvetica', 8)
        c.drawString(14*mm, h * 0.455, 'PREPARED FOR')
        c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 12)
        c.drawString(14*mm, h * 0.425, self.lead_name)
        c.setFillColor(colors.HexColor('#7A8AAA')); c.setFont('Helvetica', 9)
        c.drawString(14*mm, h * 0.40, self.lead_email)
        c.setFont('Helvetica', 8)
        c.drawString(14*mm, h * 0.365, self.date_str)
        c.drawString(14*mm, h * 0.345, 'CONFIDENTIAL · FOR RECIPIENT USE ONLY')

        # Watermark
        c.setFillColor(colors.HexColor('#142040'))
        c.setFont('Helvetica-Bold', 72)
        c.drawString(w * 0.45, 22*mm, 'SQ')
        c.setFillColor(colors.HexColor('#1A3060'))
        c.setFont('Helvetica-Bold', 11)
        c.drawString(14*mm, 14*mm, 'SimplifIQ · AI-Powered Business Intelligence')


# ── Section header band ────────────────────────────────────────────────────────
class SectionHeader(Flowable):
    def __init__(self, title, subtitle=''):
        super().__init__()
        self.title    = title
        self.subtitle = subtitle
        self.width    = CONTENT_W
        self.height   = 16*mm

    def wrap(self, *_):
        return self.width, self.height

    def draw(self):
        c = self.canv
        w = self.width
        c.setFillColor(DARK_BG)
        c.roundRect(0, 0, w, self.height, 3, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(0, 0, 3, self.height, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 11)
        c.drawString(10, self.height / 2 + 1, self.title)
        if self.subtitle:
            c.setFillColor(colors.HexColor('#7A8AAA'))
            c.setFont('Helvetica', 7.5)
            c.drawRightString(w - 8, self.height / 2 - 1, self.subtitle)


# ── Metric card ────────────────────────────────────────────────────────────────
class MetricCard(Flowable):
    def __init__(self, label, value, width=55*mm, color=ACCENT):
        super().__init__()
        self.label  = label
        self.value  = str(value) if value else '—'
        self.width  = width
        self.height = 18*mm   # taller so text has room
        self.color  = color

    def wrap(self, *_):
        return self.width, self.height

    def draw(self):
        c = self.canv
        w, h = self.width, self.height

        c.setFillColor(ACCENT_LIGHT)
        c.roundRect(0, 0, w, h, 3, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0, h - 3, w, 3, 1.5, fill=1, stroke=0)

        c.setFillColor(TEXT_SUB); c.setFont('Helvetica', 6)
        c.drawString(4, h - 10, self.label.upper())

        # Value — truncate and wrap into two lines if needed
        c.setFillColor(TEXT_MAIN); c.setFont('Helvetica-Bold', 8)
        val = self.value
        max_line = int((w - 8) / 4.5)   # approx chars per line at font size 8
        if len(val) <= max_line:
            c.drawString(4, 4, val)
        else:
            # Try to break at a comma or space
            break_at = val.rfind(',', 0, max_line)
            if break_at < 1:
                break_at = val.rfind(' ', 0, max_line)
            if break_at < 1:
                break_at = max_line
            line1 = val[:break_at].strip()
            line2 = val[break_at:].strip()
            if len(line2) > max_line:
                line2 = line2[:max_line - 1] + '…'
            c.drawString(4, 10, line1)
            c.setFont('Helvetica', 7)
            c.drawString(4, 3, line2)


# ── Bullet block ───────────────────────────────────────────────────────────────
class BulletBlock(Flowable):
    """Canvas-drawn bullet list using a filled circle (no Unicode arrows)."""
    def __init__(self, items, dot_color=ACCENT, width=None):
        super().__init__()
        self.items     = items or []
        self.dot_color = dot_color
        self._w        = width or CONTENT_W
        self.height    = len(self.items) * 12 + 4

    def wrap(self, *_):
        return self._w, self.height

    def draw(self):
        c = self.canv
        y = self.height - 12
        for item in self.items:
            # Filled circle dot — no Unicode, always renders correctly
            c.setFillColor(self.dot_color)
            c.circle(5, y + 3.5, 2.5, fill=1, stroke=0)
            c.setFillColor(TEXT_MAIN)
            c.setFont('Helvetica', 9)
            text = str(item)
            # Simple truncation — keeps layout clean
            max_chars = int((self._w - 18) / 4.8)
            if len(text) > max_chars:
                text = text[:max_chars - 1] + '…'
            c.drawString(14, y, text)
            y -= 12


# ── Styles ─────────────────────────────────────────────────────────────────────
def _styles():
    def S(name, **kw):
        return ParagraphStyle(name, **kw)
    return {
        'body':        S('body',    fontName='Helvetica',      fontSize=9,
                         textColor=TEXT_MAIN, leading=14, spaceAfter=4),
        'label':       S('label',   fontName='Helvetica-Bold', fontSize=7.5,
                         textColor=TEXT_SUB,  leading=10, spaceAfter=2),
        'execsum':     S('execsum', fontName='Helvetica',      fontSize=10,
                         textColor=TEXT_MAIN, leading=16, spaceAfter=6,
                         leftIndent=8, rightIndent=8),
        'footer_note': S('fn',      fontName='Helvetica',      fontSize=7.5,
                         textColor=TEXT_SUB,  leading=10),
    }


def _make_canvas_factory(company_name):
    def factory(filename, **kwargs):
        return HeaderFooterCanvas(filename, company_name=company_name, **kwargs)
    return factory


# ── Main builder ───────────────────────────────────────────────────────────────
def generate_pdf(lead: LeadInput, report: LeadResponse):
    try:
        os.makedirs('reports', exist_ok=True)
        safe  = lead.company.replace(' ', '_').replace('/', '-')
        filename = f"reports/{safe}_intelligence_report.pdf"

        doc = SimpleDocTemplate(
            filename, pagesize=A4,
            leftMargin=L_MARGIN, rightMargin=R_MARGIN,
            topMargin=T_MARGIN,  bottomMargin=B_MARGIN,
        )

        styles = _styles()
        story  = []
        intel  = report.intelligence
        audit  = report.audit
        now    = datetime.now().strftime('%B %d, %Y')

        # 1. Cover
        story.append(CoverPage(
            company_name=intel.company_name or lead.company,
            lead_name=lead.name, lead_email=lead.email,
            industry=intel.industry, date_str=now,
        ))
        story.append(PageBreak())

        # 2. TOC
        story.append(SectionHeader('TABLE OF CONTENTS', 'Report Navigation'))
        story.append(Spacer(1, 5*mm))
        toc_items = [
            ('01', 'Company Overview',          'Company profile, key facts, business model'),
            ('02', 'Executive Summary',          'High-level analysis and positioning'),
            ('03', 'Strengths & Advantages',     'Competitive differentiators'),
            ('04', 'Strategic Gaps',             'Opportunities for improvement'),
            ('05', 'SimplifIQ Recommendations',  'Tailored AI-driven solutions'),
            ('06', 'Growth Opportunities',        'Market expansion pathways'),
        ]
        toc_data = [[
            Paragraph(f'<font color="#4F8EF7"><b>{n}</b></font>', styles['body']),
            Paragraph(f'<b>{t}</b>', styles['body']),
            Paragraph(d, styles['footer_note']),
        ] for n, t, d in toc_items]
        toc_table = Table(toc_data, colWidths=[12*mm, 65*mm, None])
        toc_table.setStyle(TableStyle([
            ('ROWBACKGROUNDS', (0,0),(-1,-1), [WHITE, ACCENT_LIGHT]),
            ('TOPPADDING',    (0,0),(-1,-1), 5),
            ('BOTTOMPADDING', (0,0),(-1,-1), 5),
            ('LEFTPADDING',   (0,0),(-1,-1), 6),
            ('RIGHTPADDING',  (0,0),(-1,-1), 6),
        ]))
        story.append(toc_table)
        story.append(PageBreak())

        # 3. Company Overview
        story.append(SectionHeader('01 · COMPANY OVERVIEW', intel.company_name or lead.company))
        story.append(Spacer(1, 4*mm))

        # Metric cards — 3 top row, 2 bottom row so text has space
        cards_data = [
            ('Industry',       intel.industry,       ACCENT),
            ('Founded',        intel.founded,         ACCENT2),
            ('Headquarters',   intel.headquarters,    GREEN),
            ('Company Size',   intel.company_size,    AMBER),
            ('Business Model', intel.business_model,  RED_SOFT),
        ]
        card_w3 = (CONTENT_W - 2 * 3*mm) / 3
        card_w2 = (CONTENT_W - 1 * 3*mm) / 2

        row1 = [MetricCard(l, v, width=card_w3, color=c) for l, v, c in cards_data[:3]]
        row2 = [MetricCard(l, v, width=card_w2, color=c) for l, v, c in cards_data[3:]] + ['']

        cards_table = Table([row1, row2], colWidths=[card_w3]*3, hAlign='LEFT')
        cards_table.setStyle(TableStyle([
            ('LEFTPADDING',   (0,0),(-1,-1), 2),
            ('RIGHTPADDING',  (0,0),(-1,-1), 2),
            ('TOPPADDING',    (0,0),(-1,-1), 2),
            ('BOTTOMPADDING', (0,0),(-1,-1), 2),
        ]))
        story.append(cards_table)
        story.append(Spacer(1, 5*mm))

        if intel.description:
            story.append(Paragraph('<b>About</b>', styles['label']))
            story.append(Paragraph(intel.description, styles['body']))
            story.append(Spacer(1, 3*mm))

        for lbl, val in [('Target Market', intel.target_market), ('Website', intel.website)]:
            if val:
                story.append(Paragraph(f'<b>{lbl}:</b> {val}', styles['body']))
        story.append(Spacer(1, 3*mm))

        # Key services — simple bullet paragraphs (no Unicode arrow)
        if intel.key_services:
            story.append(Paragraph('<b>Key Services / Products</b>', styles['label']))
            story.append(BulletBlock(intel.key_services, dot_color=ACCENT))

        if intel.notable_products:
            story.append(Spacer(1, 3*mm))
            story.append(Paragraph('<b>Notable Products / Initiatives</b>', styles['label']))
            story.append(BulletBlock(intel.notable_products, dot_color=ACCENT2))

        story.append(PageBreak())

        # 4. Executive Summary
        story.append(SectionHeader('02 · EXECUTIVE SUMMARY'))
        story.append(Spacer(1, 5*mm))
        exec_box = Table(
            [[Paragraph(audit.executive_summary, styles['execsum'])]],
            colWidths=[CONTENT_W],
        )
        exec_box.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), ACCENT_LIGHT),
            ('LINEAFTER',     (0,0),(0,-1),  3, ACCENT),
            ('TOPPADDING',    (0,0),(-1,-1), 10),
            ('BOTTOMPADDING', (0,0),(-1,-1), 10),
            ('LEFTPADDING',   (0,0),(-1,-1), 12),
            ('RIGHTPADDING',  (0,0),(-1,-1), 12),
        ]))
        story.append(exec_box)
        story.append(Spacer(1, 8*mm))

        # 5. Strengths
        story.append(KeepTogether([
            SectionHeader('03 · STRENGTHS & COMPETITIVE ADVANTAGES', 'What they do well'),
            Spacer(1, 4*mm),
            BulletBlock(audit.strengths, dot_color=GREEN),
            Spacer(1, 6*mm),
        ]))

        # 6. Gaps
        story.append(KeepTogether([
            SectionHeader('04 · STRATEGIC GAPS IDENTIFIED', 'Areas of opportunity'),
            Spacer(1, 4*mm),
            BulletBlock(audit.potential_gaps, dot_color=AMBER),
            Spacer(1, 6*mm),
        ]))

        # 7. Recommendations
        story.append(SectionHeader('05 · SIMPLIFIQ RECOMMENDATIONS', 'Tailored AI solutions'))
        story.append(Spacer(1, 4*mm))
        recs = getattr(audit, 'simplifiq_recommendations', None) \
               or getattr(audit, 'recommended_solutions', [])
        for i, rec in enumerate(recs, 1):
            rec_row = Table([[
                Paragraph(f'<font color="#FFFFFF"><b>{i:02d}</b></font>', styles['body']),
                Paragraph(rec, styles['body']),
            ]], colWidths=[9*mm, CONTENT_W - 9*mm])
            rec_row.setStyle(TableStyle([
                ('BACKGROUND',    (0,0),(0,-1), ACCENT),
                ('LINEBELOW',     (0,0),(-1,-1), 0.5, colors.HexColor('#DADFE8')),
                ('TOPPADDING',    (0,0),(-1,-1), 5),
                ('BOTTOMPADDING', (0,0),(-1,-1), 5),
                ('LEFTPADDING',   (0,0),(-1,-1), 6),
                ('RIGHTPADDING',  (0,0),(-1,-1), 6),
                ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
            ]))
            story.append(rec_row)
        story.append(Spacer(1, 6*mm))

        # 8. Growth
        growth = getattr(audit, 'growth_opportunities', [])
        if growth:
            story.append(KeepTogether([
                SectionHeader('06 · GROWTH OPPORTUNITIES', 'Expansion pathways'),
                Spacer(1, 4*mm),
                BulletBlock(growth, dot_color=ACCENT2),
                Spacer(1, 6*mm),
            ]))

        # 9. Closing note
        story.append(HRFlowable(width='100%', thickness=0.5,
                                color=colors.HexColor('#DADFE8')))
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph(
            f"This report was generated automatically by SimplifIQ's AI research engine on {now}. "
            "All data is sourced from public information and AI analysis. "
            "For questions, contact the SimplifIQ team.",
            styles['footer_note']
        ))

        doc.build(story, canvasmaker=_make_canvas_factory(intel.company_name or lead.company))
        return {'success': True, 'path': filename}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {'success': False, 'message': str(e)}