import uvicorn
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from api import api_router
from config.settings import BaseConfig as config


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

app = FastAPI(title=config.PROJECT_NAME)

logger = logging.getLogger(__name__)
logger.info("=== APP STARTED - LOGGING CONFIGURED ===")

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
