import json
import requests
from requests.auth import HTTPBasicAuth

def get_image_ids(geojson_geometry, PLANET_API_KEY):
    # get images that overlap with our AOI 
    geometry_filter = {
      "type": "GeometryFilter",
      "field_name": "geometry",
      "config": geojson_geometry
    }

    # get images acquired within a date range
    date_range_filter = {
      "type": "DateRangeFilter",
      "field_name": "acquired",
      "config": {
        "gte": "2021-01-01T00:00:00.000Z",
        "lte": "2021-12-31T00:00:00.000Z"
      }
    }

    # only get images which have <50% cloud coverage
    cloud_cover_filter = {
      "type": "RangeFilter",
      "field_name": "cloud_cover",
      "config": {
        "lte": 0.2
      }
    }

    # combine our geo, date, cloud filters
    combined_filter = {
      "type": "AndFilter",
      "config": [geometry_filter, date_range_filter, cloud_cover_filter]
    }

    item_type = "PSScene"

    # API request object
    search_request = {
      "item_types": [item_type], 
      "filter": combined_filter
    }

    # fire off the POST request
    search_result = \
      requests.post(
        'https://api.planet.com/data/v1/quick-search',
        auth=HTTPBasicAuth(PLANET_API_KEY, ''),
        json=search_request)

    geojson = search_result.json()

    # extract image IDs only
    image_ids = [feature['id'] for feature in geojson['features']]
    return image_ids