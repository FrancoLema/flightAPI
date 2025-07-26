import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from api import api_router
from config.settings import BaseConfig as config


load_dotenv()

app = FastAPI(title=config.PROJECT_NAME)


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
