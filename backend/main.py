from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import Base, SessionLocal, engine
from routes import auth, cart, favorites, products
from schemas import HealthStatus
from seed import seed_products

app = FastAPI(title="MarketP API", version="0.1.0", description="E-commerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    # Match the OpenAPI ErrorResponse shape: { "message": ... }
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(status_code=422, content={"message": "Invalid request", "errors": exc.errors()})


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_products(db)
    finally:
        db.close()


@app.get("/api/healthz", response_model=HealthStatus, tags=["health"])
def health_check() -> HealthStatus:
    return HealthStatus(status="ok")


app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(favorites.router, prefix="/api")
