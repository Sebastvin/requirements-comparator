import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import router as api_router

app = FastAPI()

allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [
    origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
