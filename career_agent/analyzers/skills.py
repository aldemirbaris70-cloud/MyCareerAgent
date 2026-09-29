"""Rule-based technical and transferable skill extraction."""

import re


class SkillExtractor:
    """Find known skills using case-insensitive, boundary-aware matching."""

    SKILLS: tuple[str, ...] = (
        "Accessibility", "Agile", "AWS", "Azure", "C", "C#", "C++", "CI/CD",
        "Communication", "CSS", "Cybersecurity", "Data Analysis", "Data Science",
        "Django", "Docker", "Excel", "Figma", "Flask", "Git", "HTML", "Java",
        "JavaScript", "Kubernetes", "Leadership", "Linux", "Machine Learning",
        "Microsoft Office", "MongoDB", "Next.js", "Node.js", "NoSQL", "Pandas",
        " PostgreSQL", "Power BI", "Project Management", "Python", "React",
        "REST API", "SQL", "Tableau", "Teamwork", "TensorFlow", "TypeScript",
    )

    def __init__(self) -> None:
        self._patterns = {
            skill.strip(): re.compile(
                rf"(?<![\w+#.]){re.escape(skill.strip())}(?![\w+#.])", re.IGNORECASE
            )
            for skill in self.SKILLS
        }

    def extract(self, text: str) -> set[str]:
        """Return canonical skill names found in text."""
        return {skill for skill, pattern in self._patterns.items() if pattern.search(text)}