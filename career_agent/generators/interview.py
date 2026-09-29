"""Generate likely interview prompts based on job skill requirements."""

from career_agent.core.models import MatchScore


class InterviewQuestionGenerator:
    """Build general and skill-specific questions for interview practice."""

    def generate(self, score: MatchScore) -> tuple[str, ...]:
        questions = [
            "Tell me about a project that best demonstrates your fit for this role.",
            "Describe a time you had to learn a new tool or concept quickly.",
            "How do you approach debugging a problem you have not seen before?",
        ]
        for skill in score.matched_skills[:4]:
            questions.append(f"Can you walk me through a project where you used {skill}?")
        for skill in score.missing_skills[:3]:
            questions.append(
                f"What is your current experience with {skill}, and how would you ramp up?"
            )
        return tuple(questions)