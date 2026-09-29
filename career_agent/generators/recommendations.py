"""Generate actionable, evidence-led application recommendations."""

import re

from career_agent.core.models import MatchScore


class RecommendationGenerator:
    """Recommend concrete CV improvements from detected gaps."""

    def generate(self, cv_text: str, score: MatchScore, job_skill_count: int) -> tuple[str, ...]:
        recommendations: list[str] = []
        if score.missing_skills:
            recommendations.append(
                "If supported by your experience, add concrete examples for: "
                + ", ".join(score.missing_skills)
                + ". Do not list tools you have not used."
            )
        if not re.search(r"\b(experience|employment|internship)\b", cv_text, re.IGNORECASE):
            recommendations.append(
                "Add an Experience section with measurable outcomes from work, volunteering, or internships."
            )
        if not re.search(r"\b(education|degree|university|college)\b", cv_text, re.IGNORECASE):
            recommendations.append("Add an Education section with your degree, institution, and expected graduation date.")
        if not re.search(r"\b(project|portfolio)\b", cv_text, re.IGNORECASE):
            recommendations.append("Add relevant academic or personal projects and describe your individual contribution.")
        if job_skill_count == 0:
            recommendations.append(
                "The job description yielded no recognized skills; review its terminology or expand the skill dictionary."
            )
        if len(cv_text.split()) < 100:
            recommendations.append("Expand the CV with concise, specific evidence; the extracted document is unusually short.")
        if not recommendations:
            recommendations.append("Quantify relevant achievements and tailor the wording to the job description.")
        return tuple(recommendations)