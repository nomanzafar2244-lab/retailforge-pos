# Database migrations

The current portfolio baseline creates tables from SQLAlchemy metadata for zero-config demos. For a production PostgreSQL deployment, initialize Alembic in this directory and commit generated revision files.

Recommended command sequence:
```bash
alembic init migrations
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```
