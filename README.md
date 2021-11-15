# TSM Basic demo scheduler

Simple python [flask](https://flask.palletsprojects.com/en/2.0.x/) HTTP
service in developer mode to trigger the
[tsm-extractor](https://git.ufz.de/rdm-software/timeseries-management/tsm-extractor).

- No authentication
- no integrity
- no encryption
- no error handling
- no warranty

**Do not use in production!!!**.

# How to integrate

Call the one and only `/extractor/run` endpoint with *http* `POST` and a
*JSON* body containing the
[tsm-extractor](https://git.ufz.de/rdm-software/timeseries-management/tsm-extractor)
cli parameters:

```json
{
  "parser": "AnotherCustomParser",
  "target": "postgresql://postgres:postgres@postgres/postgres",
  "source": "https://example.com/",
  "thing_uuid": "ce2b4fb6-d9de-11eb-a236-125e5a40a845"
}
```

```bash
curl -v http://localhost:5000/extractor/run -d '{"parser":"AnotherCustomParser", "target":"postgresql://postgres:postgres@postgres/postgres", "source":"https://example.com/","thing_uuid":"ce2b4fb6-d9de-11eb-a236-125e5a40a845"}' -X POST -H "Content-Type: application/json"
```

***Happy parsing!***