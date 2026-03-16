## CertGraph Backend

CertGraph is a Django-based backend for modelling certification hierarchies:
vendors → products → courses → certifications, with explicit mapping layers between each level.
It exposes a clean REST API with interactive documentation to support exploration and integration.

---

## Project Overview

- **Purpose**: Provide a modular, testable backend to manage certification ecosystems and their relationships.
- **Scope**:
  - Master entities: `Vendor`, `Product`, `Course`, `Certification`
  - Mapping entities: `VendorProductMapping`, `ProductCourseMapping`, `CourseCertificationMapping`
  - REST APIs for CRUD operations and hierarchical mappings
  - Query-parameter–based filtering for common lookups
  - Swagger / ReDoc documentation and sample seed data

---

## Architecture

- **Project layout**
  - `manage.py` – Django entrypoint
  - `config/` – Django configuration package
    - `settings/base.py` – base settings (SQLite, installed apps, DRF, drf-yasg)
    - `urls.py` – root URL configuration (admin, docs, API includes)
    - `asgi.py`, `wsgi.py`
  - Domain apps:
    - `vendor/`
    - `product/`
    - `course/`
    - `certification/`
    - `vendor_product_mapping/`
    - `product_course_mapping/`
    - `course_certification_mapping/`
  - Shared app:
    - `core/base_models.py` – abstract `BaseModel` with `is_active`, `created_at`, `updated_at`
    - `core/query_params.py` – safe query-parameter helpers
    - `core/management/commands/seed_data.py` – seed command

- **Design highlights**
  - All concrete models inherit from `BaseModel` for consistent auditing and soft-delete support.
  - Mappings have database-level `UniqueConstraint`s to:
    - Prevent duplicate parent/child pairs.
    - Enforce a single `primary_mapping` per parent.
  - APIs are implemented using `APIView` only (no ViewSets/mixins/routers) for explicit control.

---

## Tech Stack

- **Language**: Python 3.11
- **Framework**: Django 5.x
- **API**: Django REST Framework
- **Documentation**: drf-yasg (Swagger UI + ReDoc)
- **Database**: SQLite (development)

Python dependencies are defined in `requirements.txt`:

- `django>=5.0,<6`
- `djangorestframework>=3.14`
- `drf-yasg>=1.21`

---

## Setup Instructions

From the project root (`D:\Fun\CertGraph`):

1. **Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Apply database migrations**

```bash
python manage.py migrate
```

4. (Optional) **Create a superuser**

```bash
python manage.py createsuperuser
```

---

## Running the Project

Start the development server:

```bash
python manage.py runserver
```

The server runs at:

- `http://127.0.0.1:8000/`

Admin interface:

- `http://127.0.0.1:8000/admin/`

---

## Swagger Documentation

Interactive API documentation is provided via drf-yasg:

- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

The documentation includes:

- Request/response schemas based on DRF serializers
- Query parameter descriptions (e.g. `vendor_id`, `product_id`, `course_id`)
- Documented error responses (validation errors, not-found conditions)

---

## Example API Requests

Base URL in examples: `http://127.0.0.1:8000`.

### Vendors

- **List vendors**

```bash
curl -X GET http://127.0.0.1:8000/api/vendors/
```

- **Create vendor**

```bash
curl -X POST http://127.0.0.1:8000/api/vendors/ ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Example Vendor\", \"code\": \"EX-VND\", \"description\": \"Demo vendor\"}"
```

### Products

- **List products (optionally filter by vendor)**

```bash
curl -X GET "http://127.0.0.1:8000/api/products/?vendor_id=1"
```

- **Create product**

```bash
curl -X POST http://127.0.0.1:8000/api/products/ ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Example Product\", \"code\": \"EX-PRD\", \"vendor\": 1}"
```

### Courses

- **List courses filtered by product**

```bash
curl -X GET "http://127.0.0.1:8000/api/courses/?product_id=2"
```

### Certifications

- **List certifications filtered by course**

```bash
curl -X GET "http://127.0.0.1:8000/api/certifications/?course_id=3"
```

### Mappings

- **List vendor-product mappings**

```bash
curl -X GET http://127.0.0.1:8000/api/vendor-product-mappings/
```

- **List product-course mappings**

```bash
curl -X GET http://127.0.0.1:8000/api/product-course-mappings/
```

- **List course-certification mappings**

```bash
curl -X GET http://127.0.0.1:8000/api/course-certification-mappings/
```

All write endpoints (`POST`, `PUT`, `PATCH`) accept JSON bodies matching their serializers as documented in Swagger/ReDoc.

---

## Seed Data Command

To help reviewers quickly test the APIs with realistic data, a management command seeds a small certification graph.

Run:

```bash
python manage.py seed_data
```

What it does:

- Clears existing:
  - Vendors, products, courses, certifications
  - All mapping tables
- Creates:
  - AWS and Azure vendors
  - Several products (security, data analytics) per vendor
  - Courses tied to those products
  - Certifications tied to courses
  - All mapping layers with primary mappings per parent

After running `seed_data`, the list endpoints and filters (e.g. `vendor_id`, `product_id`, `course_id`) will immediately return populated, realistic data for exploration. 
