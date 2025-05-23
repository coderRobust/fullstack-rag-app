"""
Main entry point for the FastAPI application.
Includes routers for authentication, document management, and Q&A.
Initializes the database and loads middleware.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from routers import auth, documents, qa
from db.init_db import init_db
from middleware.auth_middleware import AuthMiddleware

app = FastAPI(
    title="RAG Document Management and Q&A System",
    version="1.0.0",
    description="Upload documents, index them using embeddings, and ask questions via RAG pipeline"
)

# CORS config (allow frontend dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom JWT authentication middleware
app.add_middleware(AuthMiddleware)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(qa.router, prefix="/qa", tags=["Q&A"])


@app.on_event("startup")
async def on_startup():
    """Run DB setup logic and startup tasks"""
    await init_db()


@app.get("/", tags=["Health Check"])
async def root():
    """Health check endpoint"""
    return {"message": "RAG Q&A backend is running."}


# ✅ Inject BearerAuth into Swagger docs
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete"]:
                openapi_schema["paths"][path][method]["security"] = [
                    {"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
