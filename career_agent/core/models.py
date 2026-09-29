"""Typed data models passed between career-agent modules."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MatchScore:
    """A transparent ATS-style score and its component metrics."""

    overall: float
    skill_coverage: float
    section_coverage: float
    matched_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]


@dataclass
class AnalysisReport:
    """Full analysis and generated application materials for one role."""

    cv_text: str
    job_text: str
    cv_skills: tuple[str, ...]
    job_skills: tuple[str, ...]
    score: MatchScore
    optimized_cv: str
    cover_letter: str
    interview_questions: tuple[str, ...]
    recommendations: tuple[str, ...]
    candidate_name: str = ""
    company: str = ""
    metadata: dict[str, str] = field(default_factory=dict)