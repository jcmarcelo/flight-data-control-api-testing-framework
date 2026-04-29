# ✈️ Aeronautical Fleet Control — API Testing Framework

Automated API test suite simulating quality assurance workflows for an aeronautical fleet management system. Built with Python, pytest, and GitHub Actions CI/CD.

![CI](https://github.com/jcmarcelo/api-testing-framework/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![pytest](https://img.shields.io/badge/pytest-9.0-orange)
![Tests](https://img.shields.io/badge/tests-45-green)

---

## 📋 Overview

This framework simulates a QA testing environment for an aeronautical fleet control API, covering:

- **Fleet management** — aircraft registration, status updates, decommissioning
- **Flight operations** — scheduling, dispatch, cancellation, real-time status
- **MRO workflows** — maintenance orders, technician assignment, work order closure
- **Security & validation** — authentication headers, invalid payloads, negative scenarios

> The framework uses [JSONPlaceholder](https://jsonplaceholder.typicode.com) as a mock backend, replicating the structure of a real aviation REST API. In a production environment, only the `BASE_URL` in `conftest.py` would change.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| pytest | Test runner and assertion framework |
| requests | HTTP client for API calls |
| pytest-json-report | JSON output for custom reporting |
| GitHub Actions | CI/CD pipeline — runs on every push |

---

## 📁 Project Structure

```
api-testing-framework/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── tests/
│   ├── conftest.py             # Base fixtures: session, base_url
│   ├── test_aeronaves.py       # Basic fleet endpoint tests
│   ├── test_vuelos.py          # Basic flight endpoint tests
│   └── aeronautica/
│       ├── conftest.py         # Domain fixtures: aircraft, flights, MRO data
│       ├── test_vuelos_e2e.py       # End-to-end flight workflows
│       ├── test_mantenimiento.py    # MRO order management
│       ├── test_autenticacion.py    # Auth & security headers
│       ├── test_datos_invalidos.py  # Invalid payload handling
│       └── test_negativos.py        # Negative scenario testing
├── reports/                    # Auto-generated HTML dashboard (gitignored)
├── generate_report.py          # Custom bilingual HTML report generator
├── requirements.txt
└── README.md
```

---

## 🧪 Test Coverage

| Module | Tests | Type |
|---|---|---|
| `test_aeronaves.py` | 5 | Basic — status codes, schema, CRUD |
| `test_vuelos.py` | 7 | Basic — status codes, schema, CRUD |
| `test_aeronaves_e2e.py` | 11 | End-to-end fleet workflows |
| `test_vuelos_e2e.py` | 9 | End-to-end flight workflows |
| `test_mantenimiento.py` | 8 | MRO order creation and assignment |
| `test_autenticacion.py` | 4 | Security headers and auth validation |
| `test_datos_invalidos.py` | 6 | Invalid and malformed payloads |
| `test_negativos.py` | 6 | Error handling and negative scenarios |

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/jcmarcelo/api-testing-framework.git
cd api-testing-framework
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run tests**
```bash
# Run all tests
python -m pytest tests/ -v

# Run only aeronautical e2e tests
python -m pytest tests/aeronautica/ -v

# Run a specific module
python -m pytest tests/aeronautica/test_mantenimiento.py -v
```

**5. Generate custom HTML dashboard**
```bash
python generate_report.py
```
Opens `reports/report.html` — a bilingual (EN/ES) dashboard with full test results.

---

## ⚙️ CI/CD Pipeline

Every push to `main` triggers the GitHub Actions pipeline:

1. Spins up Ubuntu environment with Python 3.11
2. Installs all dependencies
3. Runs the full test suite
4. Uploads the HTML report as a build artifact

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

---

## 🔧 Adapting to a Real API

This framework is designed to be reusable. To point it at a real aviation API:

**1. Update `BASE_URL` in `tests/conftest.py`**
```python
# Mock backend (current)
BASE_URL = "https://jsonplaceholder.typicode.com"

# Real staging environment
BASE_URL = "https://staging.your-aviation-api.com"
```

**2. Add authentication if required**
```python
@pytest.fixture
def session():
    s = requests.Session()
    s.headers.update({
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_TOKEN"
    })
    return s
```

**3. Update domain fixtures in `tests/aeronautica/conftest.py`** with real aircraft registrations, flight numbers, and MRO data.

---

## 📊 Sample Report

The custom dashboard (`generate_report.py`) produces a bilingual EN/ES HTML report with:
- Pass/fail metrics
- Per-test duration
- Module breakdown
- Language toggle button

---

## 👤 Author

**Juan Carlos** · QA Engineer  
[GitHub](https://github.com/jcmarcelo) · [LinkedIn](https://linkedin.com/in/juancarlosmarcelogon)

---

*Simulated API target: [JSONPlaceholder](https://jsonplaceholder.typicode.com) — a free REST API for testing and prototyping.*
