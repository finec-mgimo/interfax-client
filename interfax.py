from contextlib import contextmanager

import xmlschema
from zeep import Client

from settings import wdsl_url, login, password, get_schema_file 

@contextmanager
def get_client(wdsl_url, login, password):
    client = Client(wdsl_url)
    client.service.Authmethod(login, password)
    try:
        yield client
    finally:
        client.service.EndAll()

with get_client(wdsl_url, login, password) as client:
    # xml-ответ по схеме СПАРКа про компанию с таким Spark ID
    # (например, 210 для Роснефти или 158, кажется, для Газпрома)
    a = client.service.GetCompanyShortReport(210).xmlData

    # Если хочется задать ИНН или ОГРН, а не СПАРК-ID, то можно указать по ключевому слову
    # Еще пример с пустыми позиционными аргументами:
    # client.service.GetCompanyAccountingReport(210, "", "", "2018-12-31").xmlData # бухгалтерская отчётность РосНефти за нужную дату
    # по идее a и b отличаются только timestamp
    b = client.service.GetCompanyShortReport(inn="7706107510").xmlData

    # с помощью схемы мы переводим XML в питоновский словарь, а его уже в JSON и в Mongo
    Schema = xmlschema.XMLSchema(get_schema_file("ShortReport.xsd"))
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

assert data['Data']['Report'][0]['INN'] == '7706107510'