# JSON Examples for MCP-OPENSTREETMAP Tools

## 1. Analyze Commute (`analyze_commute`)
```json
{
  "client_details": {
    "tool_name": "analyze_commute",
    "arguments": {
      "home_latitude": 12.9716,
      "home_longitude": 77.5946,
      "work_latitude": 12.9352,
      "work_longitude": 77.6245,
      "modes": ["car", "foot", "bike"],
      "depart_at": "09:00"
    }
  }
}
```

## 2. Geocode Address (`geocode_address`)
```json
{
  "client_details": {
    "tool_name": "geocode_address",
    "arguments": {
      "address": "1600 Amphitheatre Parkway, Mountain View, CA"
    }
  }
}
```

## 3. Find Nearby Places (`find_nearby_places`)
```json
{
  "client_details": {
    "tool_name": "find_nearby_places",
    "arguments": {
      "latitude": 12.9716,
      "longitude": 77.5946,
      "radius": 1000,
      "categories": ["amenity", "shop"],
      "limit": 10
    }
  }
}
``` 