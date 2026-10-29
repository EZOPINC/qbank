"""python manage.py dump_extraction path/to/file.pdf  -> shows raw OCR text per page + what the parser found."""
from django.core.management.base import BaseCommand
from bank.extraction.extractor import extract_document
from bank.parser import parse_pages


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("--out", default="extraction_dump.txt")

    def handle(self, *a, **o):
        pages = extract_document(o["path"])
        qs = parse_pages(pages)
        with open(o["out"], "w", encoding="utf-8") as f:
            for p in pages:
                f.write(f"===== PAGE {p.number} method={p.method} conf={p.confidence} =====\n{p.text}\n")
            f.write("\n===== PARSED =====\n")
            for q in qs:
                f.write(f'#{q["number"]} ans={q["answer"]} flags={q["flags"]} | {q["text"][:80]}\n')
        self.stdout.write(f"{len(pages)} pages, {len(qs)} questions -> {o['out']}")
