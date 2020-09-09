from settings import login, password
from interfax import Reporter

with Reporter(login, password) as reporter: 
    a = reporter.GetCompanyShortReport(sparkId=210)
    
assert a["INN"] == "7706107510"
assert a["ShortNameEn"] == "Rosneft Oil Company"