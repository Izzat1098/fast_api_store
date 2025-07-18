import os
from fastapi import FastAPI, APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from dotenv import load_dotenv
from database.seed_db import seed_database

# Load environment variables
load_dotenv()

# Database imports
from database import Base, engine

# Import models to ensure they're registered with SQLAlchemy
import app_models

# Import router modules
from store_items.routes import item_router
from orders.routes import order_router
from users.routes import user_router

# Initialize FastAPI app
app = FastAPI(
    title="Store API",
    version="1.0.0",
    description="API documentation for Store API"
)

# Create database tables on startup
Base.metadata.create_all(bind=engine)
seed_database()  # Call the seed function

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Store"}

# Setup versioned API router and include module routers
api_router = APIRouter(prefix="/v1")
api_router.include_router(item_router)
api_router.include_router(order_router)
api_router.include_router(user_router)

# Register the master router with the app
app.include_router(api_router)

# Setup OAuth2 scheme for Swagger UI login flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

# Custom OpenAPI schema with security configuration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Run the app using Uvicorn when executed directly
# if __name__ == "__main__":
def main():
    port = os.environ.get("PORT")
    host = os.environ.get("HOST")
    if not port or not host:
        raise EnvironmentError("PORT or HOST environment variable are not set")
    uvicorn.run("fastapi_app.main:app", host=host, port=int(port), reload=True)