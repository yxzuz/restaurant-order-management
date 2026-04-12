from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import settings
from app.db import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)


# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors and return user-friendly messages.
    """
    errors = exc.errors()

    # Create user-friendly error messages
    friendly_errors = []
    for error in errors:
        field = error.get("loc", [])[-1]  # Get the field name
        error_type = error.get("type", "")
        ctx = error.get("ctx", {})

        # Custom messages based on error type
        if error_type == "string_too_short":
            min_length = ctx.get("min_length", "")
            friendly_errors.append(
                f"{field.capitalize()} must be at least {min_length} characters long")
        elif error_type == "string_too_long":
            max_length = ctx.get("max_length", "")
            friendly_errors.append(
                f"{field.capitalize()} must be no more than {max_length} characters long")
        elif error_type == "missing":
            friendly_errors.append(f"{field.capitalize()} is required")
        else:
            # Fallback to original message
            friendly_errors.append(error.get("msg", "Invalid input"))

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Validation error",
            "errors": friendly_errors,
            "message": " | ".join(friendly_errors)
        },
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
async def root():
    return {"message": "Restaurant Order Management API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
