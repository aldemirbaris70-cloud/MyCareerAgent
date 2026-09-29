# MyCareerAgent

MyCareerAgent is a local Python application that helps students compare a CV with an internship or job description and prepare application materials. It reads PDF and DOCX CVs, accepts job descriptions as TXT/PDF/DOCX files or pasted text, detects known technical and transferable skills, calculates a transparent ATS-style score, and saves a Markdown report.

Generated materials are deterministic templates, not AI-generated factual claims. The CV draft preserves the supplied CV and highlights only skills found in that CV; review every draft before submitting it. The score is an aid for prioritizing edits, not a prediction of an employer's ATS result.

## Requirements

- Python 3.10 or newer
- Install document readers with `python -m pip install -r requirements.txt`

## Run

From the repository root:

```powershell
python -m pip install -r requirements.txt
python -m career_agent.main career_agent/data/sample_cv.txt career_agent/data/sample_job.txt --candidate-name "Jordan Lee" --company "Example Co"
```

For pasted job text:

```powershell
python -m career_agent.main path/to/cv.pdf --job-text "We are seeking a Python intern with SQL experience" --candidate-name "Jordan Lee"
```

The report is written to `career_agent/data/reports/` by default. Set `--output` to choose a different directory. Use `--config` to provide an alternate INI file; the default is `career_agent/config.ini`.

## Project Layout

```text
career_agent/
├── analyzers/       # Skill extraction and ATS-style scoring
├── core/            # Configuration, models, errors, and workflow
├── data/            # Sample inputs and default report destination
├── generators/      # CV, cover letter, interview, and recommendation drafts
├── parsers/         # TXT, PDF, and DOCX readers
├── reports/         # Markdown report rendering and persistence
├── tests/           # Unit and integration tests
├── config.ini
├── main.py          # CLI entry point
└── requirements.txt
```

The complete workflow is exposed through `career_agent.main` and the modular `career_agent` package.

## Tests

Run the standard-library test suite from the repository root:

```powershell
python -m unittest discover -s career_agent/tests -v
```

## Scoring

The heuristic score weights detected job-skill coverage at 85% and the presence of experience, education, and projects sections at 15%. Skills not in the built-in dictionary are not counted, and a job description without recognized skills receives zero skill coverage. This is intentionally explainable and should not be treated as an employer-specific ATS score.

## Limitations

- Scanned/image-only PDFs require OCR, which is not included.
- Skill extraction uses a maintainable built-in vocabulary and may miss synonyms or domain-specific tools.
- Generated letters and CV formatting are drafts; verify all personal details and claims.
- No cloud AI service, external account, or API key is used.