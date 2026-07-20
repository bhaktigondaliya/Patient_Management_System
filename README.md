# Patient Management System

A small REST API for storing patient records, built with FastAPI, plus a single-file HTML/React frontend to manage records from the browser.

Each patient's BMI and health verdict (Underweight / Normal / Overweight / Obese) are computed automatically from height and weight.

## Project structure

```
.
├── main.py          # FastAPI backend
├── patient.json      # Data store (flat JSON file, created automatically)
└── patient_ui.html   # Frontend — open directly in a browser, no build step
```

## Requirements

- Python 3.9+
- `fastapi`
- `uvicorn`

Install dependencies:

```bash
pip install fastapi uvicorn
```

## Running the backend

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive API docs (Swagger UI) are auto-generated at `http://127.0.0.1:8000/docs`.

> **First run:** the app expects a `patient.json` file to exist in the same directory. If it's missing, `/view` and other read endpoints will error. Create an empty one first:
> ```bash
> echo "{}" > patient.json
> ```

## Running the frontend

No install, no build step. With the backend running:

1. Keep `patient_ui.html` in the same folder as `main.py`.
2. Double-click it (or open it) in your browser.

The page talks directly to `http://127.0.0.1:8000` via `fetch`. CORS is enabled in `main.py` via `CORSMiddleware`, which is what allows a page opened from disk (or a different port) to call the API.

## API reference

| Method | Endpoint                | Description                                             |
|--------|--------------------------|-----------------------------------------------------------|
| GET    | `/`                      | Health check message                                       |
| GET    | `/about`                 | API description                                            |
| GET    | `/view`                  | Return all patients, keyed by ID                            |
| GET    | `/patient/{ids}`         | Return one or more patients by ID, comma-separated (`P001,P002`) |
| GET    | `/sort`                  | Sort patients by `id`, `name`, `city`, `age`, `gender`, `height`, `weight`, or `bmi`, `asc`/`desc` |
| POST   | `/create`                | Create a new patient                                        |
| PUT    | `/edit/{patient_id}`     | Partially update an existing patient (any subset of fields)  |
| DELETE | `/delete/{patient_id}`   | Delete a patient by ID                                       |

### Patient fields

| Field    | Type              | Notes                                  |
|----------|-------------------|------------------------------------------|
| id       | string            | Required on create, e.g. `P001`         |
| name     | string            | Required                                 |
| city     | string            | Required                                 |
| age      | int               | 1–119                                    |
| gender   | `male`/`female`/`others` | Required                          |
| height   | float             | In meters                                |
| weight   | float             | In kilograms                             |
| bmi      | float (computed)  | `weight / height²`, read-only            |
| verdict  | string (computed) | Derived from `bmi`, read-only            |

## Known limitations

- **Storage is a single JSON file**, not a database — fine for local use and testing, not for concurrent/multi-user production use.
- **No authentication** — anyone who can reach the API can read, edit, or delete any record.
- Sorting by `id` only works correctly if `id` is stored inside each patient's record (not excluded on save) — otherwise every patient falls back to the same sort value and the order won't change.

## Frontend notes

`patient_ui.html` is a single self-contained file — React, ReactDOM, and Babel are loaded from a CDN, and JSX is transpiled in the browser. It covers all six endpoints as tabs: **All patients**, **Find**, **Sort**, **Add**, **Update**, **Delete**.
