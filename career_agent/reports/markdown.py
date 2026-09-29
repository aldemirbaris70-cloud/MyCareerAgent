"""Render and save full analysis reports as Markdown."""

import re
from datetime import datetime
from pathlib import Path

from career_agent.core.models import AnalysisReport


class MarkdownReportWriter:
    """Render and persist an analysis report with portable filenames."""

    def render(self, report: AnalysisReport) -> str:
        score = report.score
        return f"""# MyCareerAgent Job Match Report

**Candidate:** {report.candidate_name or '[Not provided]'}  
**Company:** {report.company or '[Not provided]'}  
**Generated:** {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}

## ATS Compatibility

**Overall score: {score.overall:.1f}%**  
Skill coverage: {score.skill_coverage:.1f}%  
CV section coverage: {score.section_coverage:.1f}%

### Matching skills
{self._bullets(score.matched_skills)}

### Missing skills
{self._bullets(score.missing_skills)}

## Recommendations
{self._bullets(report.recommendations)}

## ATS-Optimized CV Draft

{report.optimized_cv}

## Tailored Cover Letter

{report.cover_letter}

## Likely Interview Questions
{self._numbered(report.interview_questions)}
"""

    def save(self, report: AnalysisReport, directory: str | Path) -> Path:
        output_directory = Path(directory).expanduser()
        output_directory.mkdir(parents=True, exist_ok=True)
        label = report.candidate_name or "candidate"
        safe_label = re.sub(r"[^A-Za-z0-9_-]+", "_", label).strip("_") or "candidate"
        output_path = output_directory / f"{safe_label}_job_match.md"
        output_path.write_text(self.render(report), encoding="utf-8")
        return output_path

    @staticmethod
    def _bullets(items: tuple[str, ...]) -> str:
        return "\n".join(f"- {item}" for item in items) if items else "- None detected"

    @staticmethod
    def _numbered(items: tuple[str, ...]) -> str:
        return "\n".join(f"{index}. {item}" for index, item in enumerate(items, 1))