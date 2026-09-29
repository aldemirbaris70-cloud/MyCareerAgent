"""Coordinate parsing, analysis, generation, and report creation."""

import logging
from pathlib import Path

from career_agent.analyzers.scorer import ATSScorer
from career_agent.analyzers.skills import SkillExtractor
from career_agent.core.errors import InputValidationError
from career_agent.core.models import AnalysisReport
from career_agent.generators.cover_letter import CoverLetterGenerator
from career_agent.generators.interview import InterviewQuestionGenerator
from career_agent.generators.recommendations import RecommendationGenerator
from career_agent.generators.resume import ResumeOptimizer
from career_agent.parsers.documents import DocumentParser

logger = logging.getLogger(__name__)


class CareerAgent:
    """Run the end-to-end analysis for a CV and a target job description."""

    def __init__(self, parser: DocumentParser | None = None) -> None:
        self.parser = parser or DocumentParser()
        self.skill_extractor = SkillExtractor()
        self.scorer = ATSScorer()

    def analyze(
        self,
        cv_source: str | Path,
        job_source: str | Path | None = None,
        *,
        job_text: str | None = None,
        candidate_name: str = "",
        company: str = "",
    ) -> AnalysisReport:
        """Analyze inputs and generate a report without fabricating CV facts."""
        cv_content = self.parser.read(cv_source)
        if job_text is not None:
            description = job_text.strip()
        elif job_source is not None:
            description = self.parser.read(job_source)
        else:
            raise InputValidationError("Provide a job description file or pasted job text.")
        return self._analyze_text(
            cv_content, description, candidate_name=candidate_name, company=company
        )

    def analyze_uploaded(
        self,
        cv_filename: str,
        cv_content: bytes,
        job_filename: str,
        job_content: bytes,
        *,
        candidate_name: str = "",
        company: str = "",
    ) -> AnalysisReport:
        """Analyze CV and job-description bytes from an upload interface."""
        return self._analyze_text(
            self.parser.read_bytes(cv_filename, cv_content),
            self.parser.read_bytes(job_filename, job_content),
            candidate_name=candidate_name,
            company=company,
        )

    def _analyze_text(
        self,
        cv_content: str,
        description: str,
        *,
        candidate_name: str,
        company: str,
    ) -> AnalysisReport:
        if not cv_content.strip():
            raise InputValidationError("The CV contains no readable text.")
        if not description:
            raise InputValidationError("The job description is empty.")

        cv_skills = self.skill_extractor.extract(cv_content)
        job_skills = self.skill_extractor.extract(description)
        score = self.scorer.score(cv_content, cv_skills, description, job_skills)
        logger.info(
            "Analysis complete: %d CV skills, %d job skills, %.1f%% score",
            len(cv_skills), len(job_skills), score.overall,
        )
        return AnalysisReport(
            cv_text=cv_content,
            job_text=description,
            cv_skills=tuple(sorted(cv_skills)),
            job_skills=tuple(sorted(job_skills)),
            score=score,
            optimized_cv=ResumeOptimizer().generate(cv_content, score),
            cover_letter=CoverLetterGenerator().generate(
                cv_content, description, score, candidate_name, company
            ),
            interview_questions=InterviewQuestionGenerator().generate(score),
            recommendations=RecommendationGenerator().generate(
                cv_content, score, len(job_skills)
            ),
            candidate_name=candidate_name,
            company=company,
        )