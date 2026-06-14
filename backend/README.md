# MarketP Backend (FastAPI + SQLite)

Python backend implementing the API contract defined in `lib/api-spec/openapi.yaml`.
All routes are served under the `/api` prefix and match the request/response shapes
(camelCase fields) the React frontend in `artifacts/shop` expects.

## Stack

- FastAPI + Uvicorn
- SQLAlchemy 2 (ORM) + SQLite
- JWT auth (PyJWT) with bcrypt password hashing
- Pydantic v2 schemas

## Run

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

On first startup the database is created and seeded with 40 products
(Electronics x10, Clothing x10, Books x5, Home x5, Sports x5, Toys x5).

Environment variables (all optional):

- `DATABASE_URL` — SQLAlchemy URL (default `sqlite:///./marketp.db`)
- `JWT_SECRET` — token signing secret (default dev value)

## Endpoints

| Method | Path                       | Auth | Description              |
| ------ | -------------------------- | ---- | ------------------------ |
| GET    | `/api/healthz`             | no   | Health check             |
| POST   | `/api/auth/register`       | no   | Register, returns token  |
| POST   | `/api/auth/login`          | no   | Login, returns token     |
| GET    | `/api/products`            | no   | List products (`?category=`) |
| GET    | `/api/products/categories` | no   | List categories          |
| GET    | `/api/products/{id}`       | no   | Product by id            |
| GET    | `/api/cart`                | yes  | Current user's cart      |
| POST   | `/api/cart/add`            | yes  | Add item to cart         |
| POST   | `/api/cart/update`         | yes  | Update item quantity     |
| DELETE | `/api/cart/remove`         | yes  | Remove item from cart    |
| GET    | `/api/favorites`           | yes  | List favorites           |
| POST   | `/api/favorites`           | yes  | Add favorite             |
| DELETE | `/api/favorites/{id}`      | yes  | Remove favorite          |

## Frontend integration

The Vite dev server proxies `/api` to this backend. From the repo root:

```bash
# terminal 1 — backend
cd backend && . .venv/bin/activate && uvicorn main:app --port 8000

# terminal 2 — frontend
cd artifacts/shop && PORT=8080 BASE_PATH=/ pnpm run dev
```

Override the proxy target with `API_PROXY_TARGET` (default `http://localhost:8000`).
