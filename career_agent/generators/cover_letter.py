"""Generate a role-specific cover-letter draft from evidence in the CV."""

from career_agent.core.models import MatchScore


class CoverLetterGenerator:
    """Create a concise editable letter without inventing achievements."""

    def generate(
        self,
        cv_text: str,
        job_text: str,
        score: MatchScore,
        candidate_name: str = "",
        company: str = "",
    ) -> str:
        name = candidate_name.strip() or "[Your Name]"
        organization = company.strip() or "[Company]"
        role_title = next((line.strip() for line in job_text.splitlines() if line.strip()), "this opportunity")
        if score.matched_skills:
            fit_sentence = (
                "My CV highlights "
                f"{', '.join(score.matched_skills)}, which align with several of the role's needs."
            )
        else:
            fit_sentence = (
                "I am interested in this opportunity and would welcome a chance to discuss "
                "how my background could contribute to your team."
            )
        return (
            f"Dear Hiring Manager at {organization},\n\n"
            f"I am writing to apply for {role_title} at {organization}. {fit_sentence}\n\n"
            "I would be glad to discuss specific examples from my CV and learn more about the "
            "team's priorities for this position.\n\n"
            f"Thank you for your consideration.\n\nSincerely,\n{name}\n\n"
            "---\n"
            f"Role keywords detected: {', '.join(score.matched_skills + score.missing_skills) or 'None'}\n"
        )