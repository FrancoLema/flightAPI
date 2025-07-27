import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    PROJECT_NAME = os.getenv("PROJECT_NAME")
    DATABASE_URL = os.getenv("DATABASE_URL")
    MAX_FLIGHT_DATE_MONTHS = int(os.getenv("MAX_FLIGHT_DATE_MONTHS"))
    MAX_FLIGHT_DURATION_HOURS = int(os.getenv("MAX_FLIGHT_DURATION_HOURS"))
    MAX_WAITING_TIME_HOURS = int(os.getenv("MAX_WAITING_TIME_HOURS"))
