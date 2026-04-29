"""
Generate a sample client requirements PDF for testing.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import os


def create_sample_pdf():
    output_path = os.path.join(os.path.dirname(__file__), "sample_requirements.pdf")
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=20,
        spaceAfter=20,
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leading=16,
    )

    content = []

    content.append(Paragraph("Client Requirements Document", title_style))
    content.append(Paragraph("Project: NextGen E-Commerce Platform", heading_style))
    content.append(Spacer(1, 0.2 * inch))

    content.append(Paragraph("1. Executive Overview", heading_style))
    content.append(Paragraph(
        "Acme Corp requires a modern, scalable e-commerce platform to replace our aging "
        "Magento-based online store. The new platform must support 100,000+ SKUs, handle "
        "peak traffic of 50,000 concurrent users during flash sales, and integrate with "
        "our existing ERP system (SAP). We need a mobile-first responsive design with "
        "sub-2-second page load times.",
        body_style
    ))

    content.append(Paragraph("2. Core Features Required", heading_style))
    features = [
        "Multi-vendor marketplace with vendor self-service portal",
        "Advanced product search with faceted filtering and AI-powered recommendations",
        "Shopping cart with real-time inventory validation",
        "Secure checkout with Stripe, PayPal, and Apple Pay integration",
        "Customer account management with order history and wishlists",
        "Admin dashboard with real-time sales analytics and reporting",
        "Content management system for marketing pages and blog",
        "Multi-currency and multi-language support (EN, ES, FR, DE)",
        "RESTful API for mobile app and third-party integrations",
        "Automated email notifications (order confirmation, shipping, etc.)",
    ]
    for f in features:
        content.append(Paragraph(f"• {f}", body_style))

    content.append(Paragraph("3. Technical Requirements", heading_style))
    content.append(Paragraph(
        "The platform should be built using modern web technologies with a microservices "
        "architecture. We require containerized deployment (Docker/Kubernetes) on AWS with "
        "auto-scaling capabilities. The database must support both relational data (products, "
        "orders) and document storage (product descriptions, reviews). All APIs must follow "
        "REST conventions with comprehensive documentation.",
        body_style
    ))

    content.append(Paragraph("4. Performance & Security", heading_style))
    content.append(Paragraph(
        "PCI-DSS compliance is mandatory for payment processing. The system must achieve "
        "99.9% uptime SLA. Implement WAF, DDoS protection, and regular security audits. "
        "All data must be encrypted at rest and in transit. GDPR compliance for EU customers.",
        body_style
    ))

    content.append(Paragraph("5. Timeline & Budget", heading_style))
    content.append(Paragraph(
        "Target launch date is Q3 2026. We expect an initial MVP within 12 weeks, with full "
        "feature parity by week 20. Our budget range is $100,000 - $200,000 depending on "
        "the proposed tech stack and team composition. We prefer an agile delivery model "
        "with bi-weekly demos and sprint reviews.",
        body_style
    ))

    content.append(Paragraph("6. Integration Requirements", heading_style))
    content.append(Paragraph(
        "The platform must integrate with: SAP ERP for inventory and order management, "
        "Salesforce CRM for customer data, SendGrid for transactional emails, Algolia "
        "for search, Cloudinary for image management, and Google Analytics for tracking.",
        body_style
    ))

    doc.build(content)
    print(f"✅ Sample PDF created at: {output_path}")
    return output_path


if __name__ == "__main__":
    create_sample_pdf()
