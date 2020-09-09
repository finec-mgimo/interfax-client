from contextlib import contextmanager
from typing import Optional

import xmlschema  # type: ignore
from zeep import Client  # type: ignore

from settings import ENDPOINT, login, password, locate_schema_file


@contextmanager
def get_client(
    login: Optional[str], password: Optional[str], wdsl_url: str = ENDPOINT
) -> Client:
    """Клиент для использования в конструкции with"""
    # инициализируем и авторизуемся
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


def get_short_report(client, *arg, **kwarg) -> dict:
    xml = client.service.GetCompanyShortReport(*arg, **kwarg).xmlData
    return get_schema("ShortReport.xsd").to_dict(xml)["Data"]["Report"][0]


# TODO:
# - match schemas to methods
# - generalise get_short_report()
# - list available companies


def get_schema_filename(method_name: str) -> Optional[str]:
    return dict(GetCompanyShortReport="ShortReport.xsd").get(method_name)


class Reporter:
    def __init__(self, client):
        self.client = client

    def GetCompanyShortReport(self, *arg, **kwarg):
        return get_short_report(self.client, *arg, **kwarg)


with get_client(login, password) as client:
    z = get_short_report(client, 210)
    assert z["ShortNameEn"] == "Rosneft Oil Company"
    w = Reporter(client).GetCompanyShortReport(210)
    assert z == w

with get_client(login, password) as client:
    # xml-ответ по схеме СПАРКа про компанию с таким Spark ID
    # (например, 210 для Роснефти или 158, кажется, для Газпрома)
    a = client.service.GetCompanyShortReport(210).xmlData

    # Если хочется задать ИНН или ОГРН, а не СПАРК-ID, то можно указать по ключевому слову
    # Еще пример с пустыми позиционными аргументами:
    # client.service.GetCompanyAccountingReport(210, "", "", "2018-12-31").xmlData # бухгалтерская отчётность РосНефти за нужную дату
    # по идее a и b отличаются только timestamp
    b = client.service.GetCompanyShortReport(inn="7706107510").xmlData

    # с помощью схемы мы переводим XML в питоновский словарь, а его уже в JSON и в Mongo
    Schema = xmlschema.XMLSchema(locate_schema_file("ShortReport.xsd"))
    data = Schema.to_dict(a)

# Несколько проверок
assert [x for x in data["Data"]["Report"][0].keys()] == [
    "@ActualDate",
    "SparkID",
    "CompanyType",
    "Status",
    "EGRPOIncluded",
    "IsActing",
    "DateFirstReg",
    "ShortNameRus",
    "ShortNameEn",
    "FullNameRus",
    "INN",
    "KPP",
    "OGRN",
    "OKPO",
    "FCSMCode",
    "OKATO",
    "OKTMO",
    "OKOPF",
    "OKVED2List",
    "LeaderList",
    "LegalAddresses",
    "PhoneList",
    "IndexOfDueDiligence",
    "AccessibleFinData",
    "CompanyWithSameInfo",
    "CompanyLiquidatedWithSameInfo",
]

assert data["Data"]["Report"][0]["INN"] == "7706107510"
