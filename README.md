# interfax-client
Python client to get started with Spark-Interfax SOAP API (https://www.spark-interfax.ru/integration)

### Notes

- Original intent for API is integration with other client software (like 1C), not as an end-user functionality
- We still can make use of API to cache queries in local files or a database - for recycling the queries and complex constructs of the data
- We are grateful to advice and bits of code shared by New Economic School / CEFIR who are early adopters of Interfax API for academic research

### How to use

1. You need API login and password to be able to use Spark-Interfax, save them in `.env` file in root of project folder:

```
INTERFAX_LOGIN=abc
INTERFAX_PASSWORD=zzz
```

`.env` is listed in `.gitignore`, that's why it does not get shared via Github. Keep `.gitignore` this way.

2. Install requirements:

```
pip install requirements.txt
```

3. Run `interfax.py` for simple example.
