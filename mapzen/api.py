import json
from urllib import urlencode
from urllib2 import Request, urlopen, HTTPError

from mapzen.exceptions import MapzenError, MapzenRateLimitError

__author__ = 'duydo'


def check_not_empty(reference, message=None):
    if reference:
        return reference
    raise ValueError(message)


class MapzenAPI(object):
    """
    MapzenAPI provides an implementation for search, reverse and autocomplete endpoint.
    Mapzen document https://mapzen.com/documentation/search/
    """

    DEFAULT_VERSION = 'v1'
    BASE_URL = 'https://search.mapzen.com'
    BASE_PARAMS = ('sources', 'layers', 'boundary_country')

    # Autocomplete endpoint
    AUTOCOMPLETE_API_ENDPOINT = 'autocomplete'
    AUTOCOMPLETE_API_PARAMS = BASE_PARAMS + ('text', 'focus_point_lat', 'focus_point_lon')

    # Search endpoint
    SEARCH_API_ENDPOINT = 'search'
    SEARCH_API_PARAMS = AUTOCOMPLETE_API_PARAMS + (
        'size', 'boundary_rect_min_lat', 'boundary_rect_min_lon', 'boundary_rect_max_lat', 'boundary_rect_max_lon',
        'boundary_circle_lat', 'boundary_circle_lon', 'boundary_circle_radius'
    )

    # Reverse endpoint
    REVERSE_API_ENDPOINT = 'reverse'
    REVERSE_API_PARAMS = BASE_PARAMS + ('size', 'point_lat', 'point_lon')

    # Use X-Cache to improve performance
    # Mapzen use CDN to help reduce this effect and limit the impact of common queries on its application servers.
    # See https://mapzen.com/documentation/search/api-keys-rate-limits/#caching-to-improve-performance
    x_cache = 'HIT'
    api_key = None
    version = None

    def __init__(self, api_key, version=None):
        self.api_key = check_not_empty(api_key)
        self.version = version or self.DEFAULT_VERSION

    def search(self, text, **kwargs):
        """
        Geospatial search. Finding a specific location's geographic coordinates.
        The search endpoint document: https://mapzen.com/documentation/search/search/
        Args:
            text: A location to search
            **kwargs: Optional parameters
                size: Number for results are returned. Default 10
                boundary_country: An alpha-2 or alpha-3 ISO country code
                boundary_rect_min_lat: The minimum latitude for searching within a rectangular region
                boundary_rect_min_lon: The minimum longitude for searching within a rectangular region
                boundary_rect_max_lat: The maximum latitude for searching within a rectangular region
                boundary_rect_max_lon: The maximum longitude for searching within a rectangular region
                boundary_circle_lat: The latitude for searching within a circular region
                boundary_circle_lon: The longitude for searching within a circular region
                boundary_circle_radius: The acceptable distance (kilometers) for searching within a circular region
                focus_point_lat: The latitude for places with higher scores will appear higher in the results list
                focus_point_lon: The longitude for places with higher scores will appear higher in the results list
                sources: A comma-delimited string array, such as: openstreetmap, openaddresses, whosonfirst, geonames
                layers: A comma-delimited string array, such as: venue, address, street, country, macroregion, region, macrocounty, county, locality, localadmin, borough, neighbourhood, coarse
            Returns:
                GeoJSON
            Throws:
                ValueError if input param value is invalid
                MapzenRateLimitError if rate limit exceeded
                MapzenError if any error occurs, excepts above errors
        """
        kwargs['text'] = check_not_empty(text)
        return self._make_request(
            self._prepare_endpoint(self.SEARCH_API_ENDPOINT),
            self._prepare_params(kwargs, self.SEARCH_API_PARAMS)
        )

    def reverse(self, point_lat, point_lon, **kwargs):
        """
        Reverse geocoding. Finding places or addresses near a specific latitude, longitude pair.
        The reverse geocoding document: https://mapzen.com/documentation/search/reverse/
        Args:
            point_lat: The latitude to be reversed
            point_lon: The longitude to be reversed
            **kwargs: Optional parameters
                size: Number for results will be returned.
                boundary_country: An alpha-2 or alpha-3 ISO country code
                sources: A comma-delimited string array, such as: openstreetmap, openaddresses, whosonfirst, geonames
                layers: A comma-delimited string array, such as: venue, address, street, country, macroregion, region, macrocounty, county, locality, localadmin, borough, neighbourhood, coarse
        Returns:
            GeoJSON
        Throws:
            ValueError if input param value is invalid
            MapzenRateLimitError if rate limit exceeded
            MapzenError if any error occurs, excepts above errors
        """
        kwargs['point_lat'] = point_lat
        kwargs['point_lon'] = point_lon
        return self._make_request(
            self._prepare_endpoint(self.REVERSE_API_ENDPOINT),
            self._prepare_params(kwargs, self.REVERSE_API_PARAMS)
        )

    def autocomplete(self, text, **kwargs):
        """
        Search with autocomplete.
        The Autocomplete endpoint document https://mapzen.com/documentation/search/autocomplete/
        Args:
            text: A location to search
            **kwargs: Optional parameters
                size: Number for results are returned. Default 10
                boundary_country: An alpha-2 or alpha-3 ISO country code. Searching within a country
                boundary_rect_min_lat: The minimum latitude for searching within a rectangular region
                boundary_rect_min_lon: The minimum longitude for searching within a rectangular region
                boundary_rect_max_lat: The maximum latitude for searching within a rectangular region
                boundary_rect_max_lon: The maximum longitude for searching within a rectangular region
                boundary_circle_lat: The latitude for searching within a circular region
                boundary_circle_lon: The longitude for searching within a circular region
                boundary_circle_radius: The acceptable distance (kilometers) for searching within a circular region
                focus_point_lat: The latitude for places with higher scores will appear higher in the results list
                focus_point_lon: The longitude for places with higher scores will appear higher in the results list
                sources: A comma-delimited string array, such as: openstreetmap, openaddresses, whosonfirst, geonames
                layers: A comma-delimited string array, such as: venue, address, street, country, macroregion, region, macrocounty, county, locality, localadmin, borough, neighbourhood, coarse
        Returns:
            GeoJSON
        Throws:
            ValueError if input param value is invalid
            MapzenRateLimitError if rate limit exceeded
            MapzenError if any error occurs, excepts above errors
        """
        kwargs['text'] = check_not_empty(text)
        return self._make_request(
            self._prepare_endpoint(self.AUTOCOMPLETE_API_ENDPOINT),
            self._prepare_params(kwargs, self.AUTOCOMPLETE_API_PARAMS)
        )

    def use_api_key(self, api_key):
        """Use another api key"""
        self.api_key = check_not_empty(api_key)
        return self

    def use_hit_cache(self):
        """Use X-Cache: HIT for HTTP request headers"""
        self.x_cache = 'HIT'
        return self

    def use_miss_cache(self):
        """Use X-Cache: MISS for HTTP request headers"""
        self.x_cache = 'MISS'
        return self

    def _prepare_endpoint(self, endpoint_type):
        return '%s/%s/%s' % (self.BASE_URL, self.version, endpoint_type)

    def _prepare_params(self, params, allowed_params):
        _params = {'api_key': self.api_key}
        for k, v in params.iteritems():
            if k in allowed_params:
                _params[k.replace('_', '.')] = v
        return _params

    def _make_request(self, endpoint, params):
        try:
            request = Request('%s/?%s' % (endpoint, urlencode(params)))
            request.add_header('X-Cache', self.x_cache)
            response = urlopen(request)
            return json.loads(response.read(), encoding='utf-8')
        except HTTPError as e:
            self._raise_exceptions_for_status(e)
        except Exception as e:
            raise MapzenError(str(e))

    @staticmethod
    def _raise_exceptions_for_status(e):
        status_code = e.getcode()
        reason = None
        if 400 <= status_code < 500:
            if status_code == 403:
                reason = '%s Forbidden: %s for url: %s' % (status_code, e.reason, e.geturl())
            elif status_code == 429:
                reason = '%s Too Many Requests: %s for url: %s' % (status_code, e.reason, e.geturl())
                raise MapzenRateLimitError(reason, status_code=status_code)
            else:
                reason = '%s Client Error: %s for url: %s' % (status_code, e.reason, e.geturl())
        elif 500 <= status_code < 600:
            reason = '%s Server Error: %s for url: %s' % (status_code, e.reason, e.geturl())
        if reason:
            raise MapzenError(reason, status_code=status_code)
