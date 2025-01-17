# Grab all the tickers from the PSX JSON file that are not ETFs, 
# debt securities, or GEM securities
import json

# Load the JSON data from the file
with open('psx.json', 'r') as file:
    data = json.load(file)

# Filter the tickers where isETF, isDebt, and isGEM are all false
filtered_tickers = [
    {
        'symbol': ticker['symbol'],
        'name': ticker['name'],
        'sectorName': ticker['sectorName']
    }
    for ticker in data if not ticker['isETF'] and not ticker['isDebt'] and not ticker['isGEM']
]

# Output the filtered tickers to a new JSON file
with open('tickers.json', 'w') as outfile:
    json.dump(filtered_tickers, outfile, indent=4)