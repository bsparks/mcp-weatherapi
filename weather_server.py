"""
WeatherAPI MCP Server
Provides weather data tools using the WeatherAPI.com service
"""

import os
from typing import Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weatherapi")

# Get API key from environment
API_KEY = os.getenv("WEATHERAPI_KEY")
BASE_URL = "https://api.weatherapi.com/v1"


@mcp.tool()
async def get_current_weather(location: str) -> dict:
    """
    Get current weather conditions for a location.
    
    Args:
        location: Location name, city, coordinates (lat,lon), IP address, or postal code
    
    Returns:
        Current weather data including temperature, conditions, wind, humidity, etc.
    """
    if not API_KEY:
        return {"error": "WEATHERAPI_KEY environment variable not set"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/current.json",
                params={
                    "key": API_KEY,
                    "q": location,
                    "aqi": "yes"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "location": {
                    "name": data["location"]["name"],
                    "region": data["location"]["region"],
                    "country": data["location"]["country"],
                    "lat": data["location"]["lat"],
                    "lon": data["location"]["lon"],
                    "localtime": data["location"]["localtime"]
                },
                "current": {
                    "temp_c": data["current"]["temp_c"],
                    "temp_f": data["current"]["temp_f"],
                    "condition": data["current"]["condition"]["text"],
                    "wind_kph": data["current"]["wind_kph"],
                    "wind_mph": data["current"]["wind_mph"],
                    "wind_dir": data["current"]["wind_dir"],
                    "pressure_mb": data["current"]["pressure_mb"],
                    "precip_mm": data["current"]["precip_mm"],
                    "humidity": data["current"]["humidity"],
                    "cloud": data["current"]["cloud"],
                    "feelslike_c": data["current"]["feelslike_c"],
                    "feelslike_f": data["current"]["feelslike_f"],
                    "vis_km": data["current"]["vis_km"],
                    "uv": data["current"]["uv"],
                    "air_quality": data["current"].get("air_quality", {})
                }
            }
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}


@mcp.tool()
async def get_forecast(location: str, days: int = 3) -> dict:
    """
    Get weather forecast for a location.
    
    Args:
        location: Location name, city, coordinates (lat,lon), IP address, or postal code
        days: Number of days of forecast (1-10)
    
    Returns:
        Weather forecast data including daily forecasts with hourly breakdowns
    """
    if not API_KEY:
        return {"error": "WEATHERAPI_KEY environment variable not set"}
    
    # Clamp days between 1 and 10
    days = max(1, min(10, days))
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/forecast.json",
                params={
                    "key": API_KEY,
                    "q": location,
                    "days": days,
                    "aqi": "yes",
                    "alerts": "yes"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            forecast_days = []
            for day in data["forecast"]["forecastday"]:
                forecast_days.append({
                    "date": day["date"],
                    "day": {
                        "maxtemp_c": day["day"]["maxtemp_c"],
                        "maxtemp_f": day["day"]["maxtemp_f"],
                        "mintemp_c": day["day"]["mintemp_c"],
                        "mintemp_f": day["day"]["mintemp_f"],
                        "avgtemp_c": day["day"]["avgtemp_c"],
                        "avgtemp_f": day["day"]["avgtemp_f"],
                        "condition": day["day"]["condition"]["text"],
                        "maxwind_kph": day["day"]["maxwind_kph"],
                        "totalprecip_mm": day["day"]["totalprecip_mm"],
                        "avghumidity": day["day"]["avghumidity"],
                        "daily_chance_of_rain": day["day"]["daily_chance_of_rain"],
                        "daily_chance_of_snow": day["day"]["daily_chance_of_snow"],
                        "uv": day["day"]["uv"]
                    },
                    "astro": {
                        "sunrise": day["astro"]["sunrise"],
                        "sunset": day["astro"]["sunset"],
                        "moonrise": day["astro"]["moonrise"],
                        "moonset": day["astro"]["moonset"],
                        "moon_phase": day["astro"]["moon_phase"]
                    }
                })
            
            return {
                "location": {
                    "name": data["location"]["name"],
                    "region": data["location"]["region"],
                    "country": data["location"]["country"],
                    "lat": data["location"]["lat"],
                    "lon": data["location"]["lon"]
                },
                "forecast": forecast_days,
                "alerts": data.get("alerts", {}).get("alert", [])
            }
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}


@mcp.tool()
async def search_location(query: str) -> dict:
    """
    Search for locations by name.
    
    Args:
        query: Location search query (minimum 3 characters)
    
    Returns:
        List of matching locations with their details
    """
    if not API_KEY:
        return {"error": "WEATHERAPI_KEY environment variable not set"}
    
    if len(query) < 3:
        return {"error": "Query must be at least 3 characters long"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/search.json",
                params={
                    "key": API_KEY,
                    "q": query
                }
            )
            response.raise_for_status()
            data = response.json()
            
            locations = []
            for loc in data:
                locations.append({
                    "name": loc["name"],
                    "region": loc["region"],
                    "country": loc["country"],
                    "lat": loc["lat"],
                    "lon": loc["lon"],
                    "url": loc["url"]
                })
            
            return {"locations": locations}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}


@mcp.tool()
async def get_astronomy(location: str, date: Optional[str] = None) -> dict:
    """
    Get astronomy information (sunrise, sunset, moon phases, etc.) for a location.
    
    Args:
        location: Location name, city, coordinates (lat,lon), IP address, or postal code
        date: Date in yyyy-MM-dd format (optional, defaults to today)
    
    Returns:
        Astronomy data including sunrise, sunset, moonrise, moonset, and moon phase
    """
    if not API_KEY:
        return {"error": "WEATHERAPI_KEY environment variable not set"}
    
    params = {
        "key": API_KEY,
        "q": location
    }
    
    if date:
        params["dt"] = date
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/astronomy.json",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "location": {
                    "name": data["location"]["name"],
                    "region": data["location"]["region"],
                    "country": data["location"]["country"],
                    "lat": data["location"]["lat"],
                    "lon": data["location"]["lon"]
                },
                "astronomy": {
                    "sunrise": data["astronomy"]["astro"]["sunrise"],
                    "sunset": data["astronomy"]["astro"]["sunset"],
                    "moonrise": data["astronomy"]["astro"]["moonrise"],
                    "moonset": data["astronomy"]["astro"]["moonset"],
                    "moon_phase": data["astronomy"]["astro"]["moon_phase"],
                    "moon_illumination": data["astronomy"]["astro"]["moon_illumination"]
                }
            }
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}


@mcp.tool()
async def get_air_quality(location: str) -> dict:
    """
    Get air quality data for a location.
    
    Args:
        location: Location name, city, coordinates (lat,lon), IP address, or postal code
    
    Returns:
        Air quality index and pollutant levels
    """
    if not API_KEY:
        return {"error": "WEATHERAPI_KEY environment variable not set"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/current.json",
                params={
                    "key": API_KEY,
                    "q": location,
                    "aqi": "yes"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            air_quality = data["current"].get("air_quality", {})
            
            return {
                "location": {
                    "name": data["location"]["name"],
                    "region": data["location"]["region"],
                    "country": data["location"]["country"]
                },
                "air_quality": air_quality
            }
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    # Run the server
    mcp.run()
