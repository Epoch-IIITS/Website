import asyncio
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query


class WeatherService:
    async def temperature(self, city):
        raise RuntimeError("network access is disabled in this course")


class Settings:
    timeout = 1.0


def get_settings():
    return Settings()


def get_weather():
    return WeatherService()


def create_app():
    app = FastAPI()
    # TODO: GET /weather/{city} and GET /weather
    return app
