from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, process

app = FastAPI(title="HybridETL API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(process.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to HybridETL API"}
