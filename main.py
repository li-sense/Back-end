from fastapi import FastAPI
from app.routes.api_config import api_router

from app.config.configs import settings

app = FastAPI(title=' API - Li-Sense')
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)