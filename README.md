## Commands
- `docker compose up --build -d`
- `docker compose exec app pytest .`
- `docker compose exec app pytest --cov=src --cov-report term-missing:skip-covered tests/`