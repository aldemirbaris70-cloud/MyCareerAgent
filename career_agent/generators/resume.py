"""Create a conservative, ATS-friendly CV draft from verified source content."""

from career_agent.core.models import MatchScore


class ResumeOptimizer:
    """Reformat CV content and emphasize only skills already present."""

    def generate(self, cv_text: str, score: MatchScore) -> str:
        verified_skills = ", ".join(score.matched_skills) or "No verified matching skills detected"
        return (
            "# ATS-Optimized CV Draft\n\n"
            "> This draft preserves the supplied CV and does not add unverified claims. "
            "Review formatting and replace any placeholders before applying.\n\n"
            "## Targeted Skills\n\n"
            f"{verified_skills}\n\n"
            "## Original CV Content\n\n"
            f"{cv_text.strip()}\n"
        )