import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(".") / ".env")

login = os.getenv("INTERFAX_LOGIN")
password = os.getenv("INTERFAX_PASSWORD")
ENDPOINT = "http://sparkgatetest.interfax.ru/iFaxWebService/iFaxWebService.asmx?WSDL"


def locate_schema_file(filename: str):
    return str(Path(".") / "schemas" / filename)
