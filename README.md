# WeatherAPI MCP Server

An MCP server that provides weather data tools using the [WeatherAPI.com](https://www.weatherapi.com/) service.

## Features

This MCP server provides the following tools:

- **get_current_weather**: Get current weather conditions for any location
- **get_forecast**: Get weather forecast (1-10 days) with hourly breakdowns
- **search_location**: Search for locations by name
- **get_astronomy**: Get sunrise, sunset, moon phases, and other astronomy data
- **get_air_quality**: Get air quality index and pollutant levels

## Setup

1. Get a free API key from [WeatherAPI.com](https://www.weatherapi.com/signup.aspx)

2. Set the API key as an environment variable:
   ```bash
   # Windows PowerShell
   $env:WEATHERAPI_KEY = "your_api_key_here"
   
   # Or add to your profile for persistence
   # Edit $PROFILE and add:
   # $env:WEATHERAPI_KEY = "your_api_key_here"
   ```

3. Install using uvx:
   ```bash
   uvx mcp-weatherapi
   ```

## Usage with Claude Desktop

Add this to your Claude Desktop configuration:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weatherapi": {
      "command": "uvx",
      "args": ["mcp-weatherapi"],
      "env": {
        "WEATHERAPI_KEY": "your_api_key_here"
      }
    }
  }
}
```

Or run locally:

```json
{
  "mcpServers": {
    "weatherapi": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/bsparks/mcp-weatherapi.git",
        "mcp-weatherapi"
      ],
      "env": {
        "WEATHERAPI_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Set your API key:
   ```bash
   $env:WEATHERAPI_KEY = "your_api_key_here"
   ```

4. Run the server:
   ```bash
   python weather_server.py
   ```

## Available Tools

### get_current_weather(location: str)
Get current weather conditions including temperature, wind, humidity, air quality, etc.

**Example**: `get_current_weather("London")`

### get_forecast(location: str, days: int = 3)
Get weather forecast for 1-10 days with daily summaries and hourly data.

**Example**: `get_forecast("New York", 5)`

### search_location(query: str)
Search for locations by name (minimum 3 characters).

**Example**: `search_location("Paris")`

### get_astronomy(location: str, date: Optional[str] = None)
Get astronomy information including sunrise, sunset, moonrise, moonset, and moon phases.

**Example**: `get_astronomy("Tokyo", "2025-11-07")`

### get_air_quality(location: str)
Get air quality index and pollutant levels.

**Example**: `get_air_quality("Beijing")`

## API Documentation

For more information about the WeatherAPI.com service, visit: https://www.weatherapi.com/docs/

## License

MIT
