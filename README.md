# interfax-client
Python client to get started quickly with Spark-Interfax API (https://www.spark-interfax.ru/integration)

### How to use

1. Clone this repo to your computer.

2. You will need API login and password to be able to use Spark-Interfax, save them in `.env` file in project folder:

```
INTERFAX_LOGIN=abc
INTERFAX_PASSWORD=zzz
```

`.env` is listed in `.gitignore`, to prevent sharing in Github. Keep `.gitignore` this way or you risk compromising the passwords.

3. Install requirements:

```
pip install requirements.txt
```

4. Run [`example.py`](example.py) for simple example:

```python
from settings import login, password
from interfax import Reporter

# Класс Reporter позволяет воспользоваться методами API Spark-Interfax.
# На входе нужно предоставить свой логин и пароль.
# Названия методов соотвествуют документации http://sparkgatetest.interfax.ru/iFaxWebService/.
# В академической версии доступна ограниченная часть базовых методов.
with Reporter(login, password) as reporter: 
    a = reporter.GetCompanyShortReport(sparkId=210)
    
assert a["INN"] == "7706107510"
assert a["ShortNameEn"] == "Rosneft Oil Company"
```

### Notes

- Original intent for API is integration with other client software (like 1C), not as an end-user functionality
- We still can make use of API to cache queries in local files or a database - for recycling the queries and complex constructs of the data
- We are grateful to advice and bits of code shared by New Economic School / CEFIR who are early adopters of Interfax API for academic research