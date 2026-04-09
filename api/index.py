import requests
from pprint import pprint

# Structure payload.
payload = {
	'source': 'universal',
	'url': 'https://www.metal.com/es/niobium-tantalum#NiobioTantalio',
	'parse': True,
	'parser_preset': 'MineralColtan',
	'render': 'html'
}

# Get response.
response = requests.request(
    'POST',
    'https://data.oxylabs.io/v1/queries',
    auth=('RoierWasHere_6fepU', 'w+HJwa9qinURST0'), #Your credentials go here
    json=payload,
)

# Instead of response with job status and results url, this will return the
# JSON response with results.
pprint(response.json())