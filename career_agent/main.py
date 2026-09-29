"""Command-line interface for MyCareerAgent."""

import argparse
import logging
from pathlib import Path

from career_agent.core.application import CareerAgent
from career_agent.core.config import AppConfig
from career_agent.core.errors import CareerAgentError
from career_agent.reports.markdown import MarkdownReportWriter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare a CV with a job and generate tailored application materials."
    )
    parser.add_argument("cv", help="CV document path (PDF, DOCX, or TXT)")
    parser.add_argument("job", nargs="?", help="Job description path (PDF, DOCX, or TXT)")
    parser.add_argument("--job-text", help="Job description pasted directly as text")
    parser.add_argument("--candidate-name", default="", help="Candidate name for the report and letter")
    parser.add_argument("--company", default="", help="Target company name")
    parser.add_argument("--output", help="Report output directory")
    parser.add_argument("--config", help="Optional INI configuration file")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if bool(args.job) == bool(args.job_text):
        parser.error("Provide exactly one job input: a job file or --job-text.")

    config = AppConfig.load(args.config)
    logging.basicConfig(
        level=getattr(logging, config.log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        report = CareerAgent().analyze(
            args.cv,
            args.job,
            job_text=args.job_text,
            candidate_name=args.candidate_name,
            company=args.company,
        )
        output_path = MarkdownReportWriter().save(
            report, args.output or config.report_directory
        )
    except (CareerAgentError, OSError) as error:
        parser.error(str(error))
    print(f"ATS compatibility: {report.score.overall:.1f}%")
    print(f"Matching skills: {', '.join(report.score.matched_skills) or 'None'}")
    print(f"Missing skills: {', '.join(report.score.missing_skills) or 'None'}")
    print(f"Report saved: {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())