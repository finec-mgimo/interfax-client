import xmlschema
from zeep import Client

from settings import login, password, wdsl_url

client = Client(wdsl_url)
client.service.Authmethod(login, password)

# ЕП: вопрос b чем распаковывать внутренности, если okfs архив?
okfs = client.service.GetClassifier("okfs")

# xml-ответ по схеме СПАРКа про компанию с таким Spark ID
# (например, 210 для Роснефти или 158, кажется, для Газпрома).
a = client.service.GetCompanyShortReport(210).xmlData

# Если хочется задать ИНН или ОГРН, а не СПАРК-ID, то можно указать по ключевому слову
b = client.service.GetCompanyShortReport(inn="7706107510").xmlData

# по идее a и b отличаются только timestamp

# Еще пример с пустыми позиционными аргументами:
# client.service.GetCompanyAccountingReport(210, "", "", "2018-12-31").xmlData # бухгалтерская отчётность РосНефти за нужную дату

# с помощью схемы мы переводим XML в питоновский словарь, а его уже в JSON и в Mongo
Schema = xmlschema.XMLSchema("ShortReport.xsd")
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

client.service.EndAll()

#TODO ideas:
# - обернуть открытие и закрытие сессии в контекст-менеджер
# - скопировать сюда схемы в отдельную директорию
# - определить какая статистика первоочередная и к каким учебным задачам относится:

"""
Н/п
	

Команда для API запроса
	

Вид Справки

1
	

GetEnterpreneurShortReport                
	

Краткая справка по ИП

2
	

GetCompanyExtendedReport               
	

Расширенная справка

3
	

GetCompanyAccountingReport             
	

Бухгалтерская отчетность

4
	

GetCompanyAccountingReportDateList
	

Список доступных балансов

5
	

GetBankAccountingReport101102       
	

101 и 102 бухгалтерской отчетности банка

6
	

GetCompanyArbitrationSummary        
	

Расширенная статистика по арбитражным судам по юридическому лицу

7
	

GetEntrepreneurArbitrationSummary 
	

Расширенная статистика по арбитражным судам по ИП

8
	

GetCompanyStateContracts                  
	

Получить список государственных контрактов компании

9
	

GetSupplierStateContracts                    
	

Получить сведения об опыте поставщика по госконтрактам

10
	

GetEntrepreneurStateContracts           
	

Получить список государственных контрактов ИП

11
	

GetStateContractReport                        
	

Получить детальную информацию по контракту

12
	

GetCompanyFinancialAnalysis               
	

Финансовый анализ компании на основе годовой бух. отчетности

13
	

GetCompanyPaymentDiscipline            
	

Данные по платежной дисциплине компании

14
	

GetTenderReport                                    
	

Детализированная информация по тендеру или госконтракту

15
	

GetEnterpreneurShortReport               
	

Краткая справка по ИП

16
	

GetCompanyExtendedReport               
	

Расширенная справка

17
	

GetCompanyAccountingReport             
	

Бухгалтерская отчетность

18
	

GetCompanyAccountingReportDateList
	

Список доступных балансов

19
	

GetCompanyStructure
	

Структура компании

"""    