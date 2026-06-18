"""
Report generation module - Creates PDF and text reports
"""

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import logging
from modules.llm_utils import sanitize_for_pdf

logger = logging.getLogger(__name__)

def generate_pdf_report(filename, review, recommendation, scores=None):
    """
    Generate a professional PDF report
    
    Args:
        filename: Output PDF filename
        review: Review text content
        recommendation: Final recommendation
        scores: Optional dict with Novelty, Technical, Clarity, Significance scores
    """
    try:
        pdf = SimpleDocTemplate(filename, pagesize=(8.5*inch, 11*inch))
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            spaceBefore=12,
        )
        
        content = []
        
        # Title
        content.append(Paragraph("AI Conference Paper Review Report", title_style))
        content.append(Spacer(1, 0.3*inch))
        
        # Recommendation box
        if scores:
            rec_table = Table([
                ['Novelty', f"{scores.get('novelty', 0)}/10"],
                ['Technical Quality', f"{scores.get('technical', 0)}/10"],
                ['Clarity', f"{scores.get('clarity', 0)}/10"],
                ['Significance', f"{scores.get('significance', 0)}/10"],
                ['Recommendation', recommendation]
            ])
            rec_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (1, 3), colors.HexColor('#e0e7ff')),
                ('BACKGROUND', (0, 4), (1, 4), colors.HexColor('#fca5a5') if recommendation == 'Reject' else colors.HexColor('#d1fae5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(rec_table)
            content.append(Spacer(1, 0.3*inch))
        
        # Detailed Review
        content.append(Paragraph("Detailed Review", heading_style))
        
        # Sanitize and format review
        clean_review = sanitize_for_pdf(review)
        
        for line in clean_review.split("\n"):
            if line.strip():
                if line.startswith("**"):
                    content.append(Paragraph(line.strip(), styles['Heading3']))
                elif line.startswith("#"):
                    content.append(Paragraph(line.replace("#", "").strip(), heading_style))
                else:
                    content.append(Paragraph(line.strip(), styles['BodyText']))
            content.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        pdf.build(content)
        logger.info(f"PDF report generated: {filename}")
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}")
        raise

def generate_text_report(review, recommendation, scores=None, metadata=None):
    """
    Generate a plain text report
    
    Args:
        review: Review text
        recommendation: Recommendation
        scores: Optional score dict
        metadata: Optional metadata dict
    
    Returns:
        str: Formatted text report
    """
    report = []
    report.append("=" * 70)
    report.append("AI CONFERENCE PAPER REVIEW REPORT")
    report.append("=" * 70)
    report.append("")
    
    if metadata:
        report.append("METADATA")
        report.append("-" * 70)
        for key, value in metadata.items():
            report.append(f"{key}: {value}")
        report.append("")
    
    if scores:
        report.append("SCORES")
        report.append("-" * 70)
        report.append(f"Novelty:              {scores.get('novelty', 0)}/10")
        report.append(f"Technical Quality:    {scores.get('technical', 0)}/10")
        report.append(f"Clarity:              {scores.get('clarity', 0)}/10")
        report.append(f"Significance:         {scores.get('significance', 0)}/10")
        avg = (scores.get('novelty', 0) + scores.get('technical', 0) + 
               scores.get('clarity', 0) + scores.get('significance', 0)) / 4
        report.append(f"Overall Score:        {avg:.1f}/10")
        report.append("")
    
    report.append("RECOMMENDATION")
    report.append("-" * 70)
    report.append(recommendation)
    report.append("")
    
    report.append("DETAILED REVIEW")
    report.append("-" * 70)
    report.append(review)
    report.append("")
    report.append("=" * 70)
    report.append("Generated by AI Conference Paper Reviewer")
    report.append("=" * 70)
    
    return "\n".join(report)
