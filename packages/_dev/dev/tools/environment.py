"""Contributor environment."""

import subprocess
from collections.abc import Iterable
from contextlib import chdir, nullcontext
from io import StringIO
from pathlib import Path
from shlex import quote
from sys import executable

import dev
from dev.modules import get_module_name
from dotenv import load_dotenv
from pydantic_settings import (
    BaseSettings,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)
from pydantic import BaseModel

class Constants(BaseModel):
    """Constants for {mod}`~dev.tools.environment`."""

    dev_tool_config: tuple[str, ...] = ("tool", get_module_name(dev))
    """Path to `dev` tool configuration in `pyproject.toml`."""
    pylance_version_source: str = ".pylance-version"
    """Path to Pylance version file."""
    shell: list[str] = ["pwsh", "-Command"]
    """Shell invocation for running arbitrary commands."""
    uv_run_wrapper: str = "./Invoke-Uv.ps1"
    """Wrapper of `uv run` with extra setup."""
    env: str = ".env"
    """Name of environment file."""


const = Constants()

def init_shell(path: Path | None = None) -> str:
    """Initialize shell."""
    with chdir(path) if path else nullcontext():
        environment = Environment().model_dump()
        dotenv = "\n".join(f"{k}={v}" for k, v in environment.items())
        load_dotenv(stream=StringIO(dotenv))
        return dotenv


def run(*args: str, check: bool = True, **kwds):
    """Run command."""
    sep = " "
    with nullcontext() if Path(const.uv_run_wrapper).exists() else chdir(".."):
        subprocess.run(
            check=check,
            args=[*const.shell, sep.join([const.uv_run_wrapper, *args])],
            **kwds,
        )


class Environment(BaseSettings):
    """Get environment variables from `pyproject.toml:[tool.env]`."""

    model_config = SettingsConfigDict(
        extra="allow", pyproject_toml_table_header=("tool", "env")
    )

    @classmethod
    def settings_customise_sources(cls, settings_cls, **_):  # pyright: ignore[reportIncompatibleMethodOverride]
        """Customize so that all keys are loaded despite not being model fields."""
        return (PyprojectTomlConfigSettingsSource(settings_cls),)


def escape(path: str | Path) -> str:
    """Escape a path, suitable for passing to e.g. {func}`~subprocess.run`."""
    return quote(Path(path).as_posix())
