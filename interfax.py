import xmlschema
from zeep import Client

from settings import login, password, wdsl_url

client = Client(wdsl_url)
client.service.Authmethod(login, password)

okfs = client.service.GetClassifier("okfs")

# такая штука выдаст xml-ответ по схеме СПАРКа про компанию с таким Spark ID
# (например, 210 для Роснефти или 158, кажется, для Газпрома).
a = client.service.GetCompanyShortReport(210).xmlData

# Если хочется задать ИНН, а не СПАРК-ID, то надо в каком-то другом месте
# поставить, типа ...ShortReport("", "", "INN") что ли, там у него чёткий порядок,
# и он умеет брать ИНН и ОГРН.
# a = client.service.GetCompanyAccountingReport(210, "", "", "2018-12-31").xmlData # бухгалтерская отчётность РосНефти за нужную дату

# Дальше мы этот xml с помощью схемы переводим в питоновский словарь,
# а тот уже в JSON и в Mongo.
Schema = xmlschema.XMLSchema("ShortReport.xsd")
data = Schema.to_dict(a)

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

client.service.EndAll()
