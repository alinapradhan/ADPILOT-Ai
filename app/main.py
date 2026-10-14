from fastapi import FastAPI

from api.routes import router
from core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0", description="Advertising intelligence API")
app.include_router(router)
