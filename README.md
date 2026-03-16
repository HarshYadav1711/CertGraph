# certgraph

Backend project scaffold built with Django 5, Django REST Framework, and drf-yasg, using a production-friendly `config` settings layout and SQLite for local development.

## Requirements

- Python 3.11
- pip

The Python dependencies are listed in `requirements.txt`:

- `django>=5.0,<6`
- `djangorestframework>=3.14`
- `drf-yasg>=1.21`

## Setup

From the project root:

```bash
cd D:\Fun\CertGraph
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running the project

Apply initial migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

The server will be available at `http://127.0.0.1:8000/`.

## API documentation

This project is configured with `drf-yasg` to provide interactive API documentation:

- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

No application APIs are implemented yet; the documentation endpoints serve the generated (currently empty) OpenAPI schema.
