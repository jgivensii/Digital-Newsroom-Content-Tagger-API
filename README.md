A containerized Python backend consisting of a Flask admin API and a FastAPI
client API. The system performs topic tagging, named‑entity extraction, and
image label generation using Amazon Comprehend and Amazon Rekognition. All
results are stored deterministically in PostgreSQL.

This repository contains:

- Flask 3.x admin API (`content_api/`)
- FastAPI 0.110+ client API (`client_api/`)
- SQLAlchemy 2.0 models + Alembic migrations
- Pydantic v2 request/response validation
- boto3 client wrappers for Comprehend, Rekognition, and S3
- structlog JSON logging with correlation IDs
- pytest test suite with AWS mocks
- Dockerized API + DB stack

---

## Features

### ✔ Publication Management
- CRUD operations
- Cascade delete of articles

### ✔ Article Management
- CRUD operations
- Tag/entity extraction via Comprehend
- Status fields: `draft | published`, `pending | complete | failed`
- Deterministic JSONB storage
- Trending entities per publication

### ✔ Image Upload Pipeline
- Multipart upload
- JPG/PNG validation
- File size validation
- S3 storage + presigned URL retrieval
- Rekognition label extraction

### ✔ FastAPI Client API
- Read‑only browsing endpoints
- Browse by tag
- Browse by title
- Trending entities

### ✔ Structured Logging
- structlog JSON logs
- Per‑request correlation IDs
- /live and /ready health endpoints

### ✔ Testing
- 20+ pytest tests
- AWS mocked tests
- DB failure tests
- Validation tests

---

## Installation

### Backend Dependencies

```code
pip install .Dependencies are defined in pyproject.toml.
```
### Running Locally 
(Docker)
```code
docker compose up --buildFlask
```
API → http://localhost:5000Fast
API client → http://localhost:8000
PostgreSQL → localhost:5432

### Environment Variables

Environment variables are stored in .env.example.

Copy it:
```code
cp .env.example .env
```
### Edge Case Handling

**Comprehend Unavailable**

Article creation rejects with `status_analysis="failed"` and a `424 failed_dependency` error. This ensures no article is saved with incomplete AI metadata.

**Very Short Article Body**

Enforced via Pydantic (`min_length=1`). Zero tags/entities are allowed.

**Duplicate Tags/Entities**

Deduplication removes:

- repeated phrases

- repeated entities

- substrings

- case‑insensitive duplicates

**Zero Tags or Entities**

If confidence filtering removes everything:

- tags = []

- entities = []

**Rekognition Unavailable / Malformed Upload**

- Invalid extension → 415

- Oversized file → 413

- Empty file → 422

- Rekognition failure → structured error envelope

**Concurrent Mutations**

SQLAlchemy default behavior:

Last write wins

Cascade deletes remove articles + TagExtractionRecord

---


## ERD (Text Description)

**Publication**

- id (UUID, PK)

- name (str)

- description (str)

- created_at

- updated_atRelationships: 1 publication → many articles

**Article**

- id (UUID, PK)

- publication_id (FK → publications.id, CASCADE)

- author (str)

- title (str)

- body (text)

- status (draft/published)

- status_analysis (pending/complete/failed)

- created_at

- updated_atRelationships:

  -  1 article → 1 image

  - 1 article → 1 tag_extraction

**TagExtractionRecord**

- id (UUID, PK)

- article_id (FK → articles.id, CASCADE)

- body (text)

- tags (JSONB)

- entities (JSONB)

- ImageRecord

- id (UUID, PK)

- article_id (FK → articles.id, CASCADE, unique)

- featured_image_key (str)

- labels (ARRAY[str])

- created_at

- updated_at

- API Overview


# ERD Diagram (ASCII)

```text
+---------------------+
|   Publication       |
+---------------------+
| id (PK)             |
| name                |
| description         |
| created_at          |
| updated_at          |
+---------------------+
          |
          | 1-to-many
          |
+---------------------+
|      Article        |
+---------------------+
| id (PK)             |
| publication_id (FK) |
| author              |
| title               |
| body                |
| status              |
| status_analysis     |
| created_at          |
| updated_at          |
+---------------------+
     |           |
     |1-to-1     |1-to-1
     |           |
+---------------------+      +---------------------------+
|   ImageRecord       |      |   TagExtractionRecord     |
+---------------------+      +---------------------------+
| id (PK)             |      | id (PK)                   |
| article_id (FK)     |      | article_id (FK)           |
| featured_image_key  |      | body                      |
| labels (ARRAY)      |      | tags (JSONB)              |
| created_at          |      | entities (JSONB)          |
| updated_at          |      |                           |
+---------------------+      +---------------------------+

```

## Flask Admin API endpoint
```code
POST   /api/v1/publications
GET    /api/v1/publications
GET    /api/v1/publications/{id}
PUT    /api/v1/publications/{id}
DELETE /api/v1/publications/{id}

POST   /api/v1/publications/{id}/articles
GET    /api/v1/publications/{id}/articles
GET    /api/v1/publications/{id}/articles/{article_id}
PUT    /api/v1/articles/{article_id}
DELETE /api/v1/articles/{article_id}

POST   /api/v1/publications/{id}/articles/{article_id}/analyze
GET    /api/v1/publications/{id}/trending-entities
```
## FastAPI Client API endpoints
```code
GET /client/v1/publications
GET /client/publications/{id}
GET /client/publications/{id}/articles
GET /client/publications/{id}/articles/by-tag
GET /client/publications/{id}/articles/by-title
GET /client/publications/{id}/articles/{article_id}
GET /client/publications/{id}/trending-entities
```
---

