import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(".") / ".env")

login = os.getenv("INTERFAX_LOGIN")
password = os.getenv("INTERFAX_PASSWORD")
wdsl_url = "http://sparkgatetest.interfax.ru/iFaxWebService/iFaxWebService.asmx?WSDL"
