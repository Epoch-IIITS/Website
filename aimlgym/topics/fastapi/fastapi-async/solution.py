r"""Reference solution for FA-14 Async Endpoints and External Services.

Both endpoints await the service through `asyncio.wait_for`, so a hung upstream cannot hang the
API. The single-city endpoint maps each failure type to its status code, most specific first. The
multi-city endpoint starts every call at once and uses `return_exceptions=True` so each city's
outcome is reported separately, in request order.
"""
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


def _describe(city, result):
    if isinstance(result, asyncio.TimeoutError):
        return {"city": city, "error": "timeout"}
    if isinstance(result, LookupError):
        return {"city": city, "error": "unknown city"}
    if isinstance(result, Exception):
        return {"city": city, "error": "service error"}
    return {"city": city, "temperature": result}


def create_app():
    app = FastAPI()

    @app.get("/weather/{city}")
    async def weather(city: str,
                      service: Annotated[WeatherService, Depends(get_weather)],
                      settings: Annotated[Settings, Depends(get_settings)]):
        try:
            temp = await asyncio.wait_for(service.temperature(city), settings.timeout)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Weather service timed out")
        except LookupError:
            raise HTTPException(status_code=404, detail="Unknown city")
        except Exception:
            raise HTTPException(status_code=502, detail="Weather service error")
        return {"city": city, "temperature": temp}

    @app.get("/weather")
    async def weather_many(city: Annotated[list[str], Query(min_length=1)],
                           service: Annotated[WeatherService, Depends(get_weather)],
                           settings: Annotated[Settings, Depends(get_settings)]):
        coros = [asyncio.wait_for(service.temperature(c), settings.timeout) for c in city]
        results = await asyncio.gather(*coros, return_exceptions=True)
        return [_describe(c, r) for c, r in zip(city, results)]

    return app
