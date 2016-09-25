Python Client for Mapzen APIs
=============================

A Python client for the Mapzen APIs.

## Mapzen Features
* Forward geocoding to find a place by searching for an address or name
* Reverse geocoding to find what is located at a certain coordinate location
* Autocomplete to give real-time result suggestions without having to type the whole location
* Global coverage with prioritized local results

## Installation

```
pip install git+https://github.com/duydo/python-mapzen.git
```

## Usage
```
from mapzen.api import MapzenAPI

api_key = 'your api_key'
api = MapzenAPI(api_key)

# Search a specific location
# r = api.search('Ho Chi Minh')

# Search within Vietnam
r = api.search(
    'Ho Chi Minh',
    boundary_country='VN'
)

# Search within Vietnam and place types: country, region or locality (towns, hamlets, cities)
r = api.search(
    'Ho Chi Minh',
    boundary_country='VN',
    layers='country,region,locality'
)

# Reverse geocoding
r = api.reverse(48.858268, 2.294471)


# Autocomeplete
r = api.autocomplete('Ho Chi Minh')
```

## Licence
```
This software is licensed under the Apache License, version 2 ("ALv2"), quoted below.

Copyright 2016 Duy Do

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
```

