from rich.traceback import install as rich_tcbck_install
rich_tcbck_install()
#============================#

import toml
from pathlib import Path
import logging
from rich.logging import RichHandler
from datetime import datetime
import getpass
import platform
from _classes import PyProjectError

def _get_project_name() -> str:
    pyproject = toml.load(Path("./pyproject.toml"))
    return pyproject["project"]["name"]

# ensure logs directory exists and add a file handler alongside the RichHandler
logs_dir = Path("./logs")
logs_dir.mkdir(parents=True, exist_ok=True)
log_file = f"logs/{_get_project_name()}-{datetime.now().strftime("%d%m%Y%H%M%S")}-{platform.node()}.log"

file_handler = logging.FileHandler(Path(log_file), encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s @ %(name)s | %(levelname)s | %(message)s")
file_handler.setFormatter(file_formatter)

console_handler = RichHandler(rich_tracebacks=True)
console_handler.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[console_handler, file_handler]
)

l = logging.getLogger(_get_project_name())
l.debug("Logger initialized.")

def check_pyproject(path: Path = Path("./pyproject.toml")):
    l.debug(f"Checking pyproject.toml at: \"{path.resolve()}\"")
    pyproject = toml.load(path)

    if pyproject["project"]["name"] == "YOURPROJECTNAME":
        l.error("The 'name' field in pyproject.toml is not set.")
        raise PyProjectError("Please update the 'name' field in pyproject.toml to your project's name.")
    if pyproject["project"]["version"] == "0.0.0":
        l.error("The 'version' field in pyproject.toml is not set.")
        raise PyProjectError("Please update the 'version' field in pyproject.toml to your project's version.")
    if pyproject["project"]["description"] == "YOURPROJECTDESCRIPTION":
        l.error("The 'description' field in pyproject.toml is not set.")
        raise PyProjectError("Please update the 'description' field in pyproject.toml to your project's description.")
    


# ==== MAIN ==== #
check_pyproject(Path("./pyproject.toml"))
