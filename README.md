# interfax-client
Python client to get started quickly with Spark-Interfax SOAP API (https://www.spark-interfax.ru/integration)

### Notes

- Original intent for API is integration with other client software (like 1C), not as an end-user functionality
- We still can make use of API to cache queries in local files or a database - for recycling the queries and complex constructs of the data
- We are grateful to advice and bits of code shared by New Economic School / CEFIR who are early adopters of Interfax API for academic research

### How to use

1. Clone this repo to your computer.

2. You need API login and password to be able to use Spark-Interfax, save them in `.env` file in project folder:

```
INTERFAX_LOGIN=abc
INTERFAX_PASSWORD=zzz
```

`.env` is listed in `.gitignore`, to prevent sharing in Github. Keep `.gitignore` this way or you risk compromising the passwords.

3. Install requirements:

```
pip install requirements.txt
```

4. Run [`interfax.py`](interfax.py) for simple example.
