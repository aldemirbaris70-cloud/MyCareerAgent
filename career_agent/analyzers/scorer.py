"""Transparent ATS-style compatibility scoring."""

import re

from career_agent.core.models import MatchScore


class ATSScorer:
    """Score skill overlap (85%) and presence of common CV sections (15%)."""

    SECTION_PATTERNS: tuple[tuple[str, str], ...] = (
        ("experience", r"\b(experience|employment|internship)\b"),
        ("education", r"\b(education|degree|university|college)\b"),
        ("projects", r"\b(projects?|portfolio)\b"),
    )

    def score(
        self, cv_text: str, cv_skills: set[str], job_text: str, job_skills: set[str]
    ) -> MatchScore:
        """Return score from 0 to 100 with skill and section details."""
        matched = tuple(sorted(cv_skills & job_skills))
        missing = tuple(sorted(job_skills - cv_skills))
        skill_coverage = len(matched) / len(job_skills) if job_skills else 0.0
        present_sections = sum(
            bool(re.search(pattern, cv_text, re.IGNORECASE))
            for _, pattern in self.SECTION_PATTERNS
        )
        section_coverage = present_sections / len(self.SECTION_PATTERNS)
        # A role without recognized skills should not receive a misleading skill score.
        overall = 100 * (0.85 * skill_coverage + 0.15 * section_coverage)
        return MatchScore(
            overall=round(overall, 1),
            skill_coverage=round(skill_coverage * 100, 1),
            section_coverage=round(section_coverage * 100, 1),
            matched_skills=matched,
            missing_skills=missing,
        )