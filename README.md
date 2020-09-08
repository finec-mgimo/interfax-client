# interfax-client
Python client to get started with Interfax Spark SOAP API (https://www.spark-interfax.ru/integration)

### Notes

- Original intent for API is integration with other client software (like 1C), not an end-user functionality (that is why it is SOAP/XML probably)
- We still can make use of API to cache queries in local files or a database - for recycling the queries and complex constructs of the data
- We are grateful to advice and bits of code shared by New Economic School / CEFIR who are early adopters of Interfax API for academic research

### How to use

You need API login and password to be able to use this software, save them in `.env` file in root of project folder:

```
INTERFAX_LOGIN=abc
INTERFAX_PASSWORD=zzz
```

