"""Load application settings from a small INI configuration file."""

import configparser
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Runtime settings with safe defaults for local use."""

    log_level: str = "INFO"
    report_directory: Path = Path("career_agent/data/reports")

    @classmethod
    def load(cls, path: str | Path | None = None) -> "AppConfig":
        config_path = Path(path) if path else Path(__file__).resolve().parents[1] / "config.ini"
        parser = configparser.ConfigParser()
        if config_path.exists():
            parser.read(config_path, encoding="utf-8")
        return cls(
            log_level=parser.get("app", "log_level", fallback="INFO").upper(),
            report_directory=Path(
                parser.get("app", "report_directory", fallback="career_agent/data/reports")
            ),
        )