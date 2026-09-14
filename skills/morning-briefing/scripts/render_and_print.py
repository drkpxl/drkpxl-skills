#!/usr/bin/env python3
"""Render HTML to PDF via WeasyPrint and send to a CUPS printer.

Usage:
  python3 render_and_print.py --html /tmp/briefing.html --pdf /tmp/briefing.pdf --printer <your_printer>
  python3 render_and_print.py --html /tmp/briefing.html --pdf /tmp/briefing.pdf --check-only

On macOS, sets DYLD_LIBRARY_PATH=/opt/homebrew/lib automatically so WeasyPrint
can find pango/glib from Homebrew.

Exits 0 on success, 1 on render failure, 2 on print failure.
"""
import os, sys, argparse, subprocess

# macOS: WeasyPrint needs pango/glib from Homebrew. Set this BEFORE importing weasyprint.
if sys.platform == 'darwin':
    os.environ.setdefault('DYLD_LIBRARY_PATH', '/opt/homebrew/lib')

from weasyprint import HTML


def render_pdf(html_path: str, pdf_path: str) -> int:
    """Render HTML to PDF, return page count."""
    doc = HTML(filename=html_path).render()
    page_count = len(doc.pages)
    doc.write_pdf(pdf_path)
    return page_count


def print_pdf(pdf_path: str, printer: str) -> tuple:
    """Send PDF to CUPS printer via lp. Return (exit_code, output)."""
    result = subprocess.run(
        ['lp', '-d', printer, '-o', 'media=letter', pdf_path],
        capture_output=True, text=True
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode, output


def main():
    parser = argparse.ArgumentParser(description='Render HTML to PDF and print')
    parser.add_argument('--html', required=True, help='Path to HTML file')
    parser.add_argument('--pdf', required=True, help='Path to output PDF')
    parser.add_argument('--printer', required=True, help='CUPS printer name')
    parser.add_argument('--check-only', action='store_true', help='Only render and check page count, do not print')
    args = parser.parse_args()

    # Render PDF
    try:
        page_count = render_pdf(args.html, args.pdf)
    except Exception as e:
        print(f'RENDER_ERROR: {e}', file=sys.stderr)
        sys.exit(1)

    size = os.path.getsize(args.pdf)
    print(f'PDF_OK: {args.pdf} ({size} bytes, {page_count} page{"s" if page_count != 1 else ""})')

    if page_count > 1:
        print(f'PAGE_OVERFLOW: {page_count} pages — needs trimming to fit 1 page', file=sys.stderr)

    if args.check_only:
        print(f'PAGES: {page_count}')
        sys.exit(0)

    # Print
    exit_code, output = print_pdf(args.pdf, args.printer)
    if exit_code != 0:
        print(f'PRINT_ERROR: lp exited {exit_code}: {output}', file=sys.stderr)
        sys.exit(2)

    print(f'PRINT_OK: {output}')
    print(f'DONE: {page_count} page(s) printed to {args.printer}')


if __name__ == '__main__':
    main()
