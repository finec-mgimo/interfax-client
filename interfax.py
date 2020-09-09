from contextlib import contextmanager
from typing import Optional

import xmlschema  # type: ignore
from zeep import Client  # type: ignore

from settings import ENDPOINT, locate_schema_file


@contextmanager
def get_client(login, password, wdsl_url=ENDPOINT) -> Client:
    """Клиент для использования в конструкции with"""
    client = Client(wdsl_url)
    client.service.Authmethod(login, password)
    try:
        # передаем в with
        yield client
    finally:
        # закрываем сессию
        client.service.End()


def get_schema(filename: str) -> xmlschema.XMLSchema10:
    return xmlschema.XMLSchema(locate_schema_file(filename))


def create_getter(method_name, schema_filename, finalise_with):
    def getter(client, *arg, **kwarg):
        xml = client.service[method_name](*arg, **kwarg).xmlData
        data = get_schema(schema_filename).to_dict(xml)
        return finalise_with(data)

    return getter


def just_one(x):
    return x["Data"]["Report"][0]


get_short_report = create_getter("GetCompanyShortReport", "ShortReport.xsd", just_one)
# FIXME
# get_company_extended_report = create_getter("GetCompanyShortReport", "ShortReport.xsd", just_one)
# get_company_accounting_report = create_getter("GetCompanyShortReport", "ShortReport.xsd", just_one)


class Reporter:
    """Класс Reporter позволяет воспользоваться методами API Spark-Interfax.
       На входе нужно предоставить свой логин и пароль.
       Названия методов соотвествуют документации http://sparkgatetest.interfax.ru/iFaxWebService/.
       В академической версии API доступна ограниченная часть методов 
       (см. https://github.com/finec-mgimo/interfax-client/issues/2)
    """

    wdsl_url = ENDPOINT
    """
    Класс для логина и получения данных:
       - иницализируется парой логин-пароль
       - одноименные методы с SOAP API Spark-Interfax
    """

    def __init__(self, login: Optional[str], password: Optional[str]):
        self.client = Client(self.wdsl_url)
        self.enter = lambda: self.client.service.Authmethod(login, password)

    def __enter__(self):
        self.enter()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.service.End()

    def GetCompanyShortReport(self, *arg, **kwarg):
        return get_short_report(self.client, *arg, **kwarg)


# Методы, работа с которым открыта образовательным организациям

available_methods = [
    ("GetEnterpreneurShortReport", "Краткая справка по ИП"),
    ("GetCompanyExtendedReport", "Расширенная справка"),
    ("GetCompanyAccountingReport", "Бухгалтерская отчетность"),
    ("GetCompanyAccountingReportDateList", "Список доступных балансов"),
    ("GetBankAccountingReport101102", "101 и 102 бухгалтерской отчетности банка"),
    (
        "GetCompanyArbitrationSummary",
        "Расширенная статистика по арбитражным судам по юридическому лицу",
    ),
    (
        "GetEntrepreneurArbitrationSummary",
        "Расширенная статистика по арбитражным судам по ИП",
    ),
    ("GetCompanyStateContracts", "Получить список государственных контрактов компании"),
    (
        "GetSupplierStateContracts",
        "Получить сведения об опыте поставщика по госконтрактам",
    ),
    ("GetEntrepreneurStateContracts", "Получить список государственных контрактов ИП"),
    ("GetStateContractReport", "Получить детальную информацию по контракту"),
    (
        "GetCompanyFinancialAnalysis",
        "Финансовый анализ компании на основе годовой бух. отчетности",
    ),
    ("GetCompanyPaymentDiscipline", "Данные по платежной дисциплине компании"),
    ("GetTenderReport", "Детализированная информация по тендеру или госконтракту"),
    ("GetEnterpreneurShortReport", "Краткая справка по ИП"),
    ("GetCompanyExtendedReport", "Расширенная справка"),
    ("GetCompanyAccountingReport", "Бухгалтерская отчетность"),
    ("GetCompanyAccountingReportDateList", "Список доступных балансов"),
    ("GetCompanyStructure", "Структура компании"),
]
