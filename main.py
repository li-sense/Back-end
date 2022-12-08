from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api_config import api_router

from app.config.configs import settings

app = FastAPI(title=' API - Li-Sense')

# Cors Config
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Config Rotas
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level='info', reload=True)
