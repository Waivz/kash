import json
import base64
from pathlib import Path
from jinja2 import Template
try:
    from weasyprint import HTML  # type: ignore
except ImportError:
    HTML = None


def render_html(context: dict, template_path: str) -> str:
    template_text = Path(template_path).read_text()
    template = Template(template_text)
    return template.render(**context)


def html_to_pdf(html: str) -> bytes:
    if HTML is None:
        raise RuntimeError("WeasyPrint not installed")
    pdf = HTML(string=html).write_pdf()
    return pdf


def encode_b64(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')


def main(json_input: str, template_path: str = 'PDF_TEMPLATE.html'):
    context = json.loads(Path(json_input).read_text())
    html = render_html(context, template_path)
    b64_html = encode_b64(html.encode('utf-8'))
    try:
        pdf_bytes = html_to_pdf(html)
        b64_pdf = encode_b64(pdf_bytes)
    except Exception as exc:
        print(f"PDF generation failed: {exc}")
        b64_pdf = ''
    print(f"[👉 View HTML Report](data:text/html;base64,{b64_html})")
    if b64_pdf:
        print(f"[📄 Download PDF](data:application/pdf;base64,{b64_pdf})")
    else:
        print("PDF generation failed")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate Cash(k) report links')
    parser.add_argument('json_input', help='Path to JSON file with report data')
    parser.add_argument('--template', default='PDF_TEMPLATE.html', help='Path to HTML template')
    args = parser.parse_args()
    main(args.json_input, args.template)
