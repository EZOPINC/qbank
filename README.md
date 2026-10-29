# Question Bank Import & Management (Django + PostgreSQL)

## Setup
```bash
sudo apt install tesseract-ocr tesseract-ocr-ben tesseract-ocr-hin   # OCR engines + Bengali/Hindi data
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d                       # PostgreSQL (+ Redis for background workers)
python manage.py makemigrations bank && python manage.py migrate
python manage.py createsuperuser
python manage.py runserver                 # http://localhost:8000  (log in, upload sample/*.pdf)
```
Add exam categories (WBCS, PSC, SSC, Clerkship) in /admin/.

Background processing: `CELERY_EAGER=0 celery -A config worker -l info` (default is eager/in-process for easy dev).

## Tests
```bash
python manage.py test bank
```
(Needs the PostgreSQL container running; Django creates a throwaway test DB.)

## Layout
- `bank/extraction/` – PDF text (pdfplumber, column-aware) + pluggable OCR (`OCR_PROVIDER` setting; Tesseract default)
- `bank/parser.py`, `normalize.py` – structuring, tags, answer-sheet mapping, language detection, dedupe hash
- `bank/validators.py` – field-level errors/warnings; `bank/importer.py` – transactional import
- `StagedQuestion` (editable, keeps `original`) -> `Question` (+ `ExamCategory` M2M, `PreviousYearRef` rows)

## Known MVP limits
Bilingual side-by-side pairing, math/LaTeX recovery from scans, explanations extraction, per-file ACL
serving and a DRF API are not implemented yet. Chapter-title lines are skipped by heuristics; check
anything flagged "Needs Review".
