"""
This script processes financial data from a JSON file and calculates the Compounded Annual Growth Rate (CAGR) 
for Earnings Per Share (EPS) and Sales for various companies. The steps involved are:

1. Load the JSON data from a file.
2. Create a pandas DataFrame from the JSON data.
3. Extract and rename relevant columns for better readability.
4. Ensure EPS and Sales columns are lists of strings.
5. Parse the current EPS value.
6. Calculate the CAGR for EPS and Sales.
7. Sort the DataFrame by the highest EPS CAGR values.
8. Save the processed DataFrame to a CSV file.

The script outputs the path to the saved CSV file containing the analysis results.
"""
import pandas as pd
import json

def calculate_cagr(values):
    """Calculate the Compounded Annual Growth Rate (CAGR)."""
    values = [v for v in values if v is not None and v != 0]
    if len(values) < 2 or values[0] < 0 or values[-1] < 0:
        return 0.0
    n = len(values) - 1
    try:
        return (values[-1] / values[0]) ** (1 / n) - 1
    except:
        return 0.0

def parse_value(value):
    """Convert string value to float, handling negative values in brackets."""
    if not value:
        return 0.0
    try:
        value = value.replace('(', '-').replace(')', '')
        return float(value)
    except ValueError:
        return 0.0

# Load the JSON data
with open('analysis/scraped_data.json') as f:
    data = json.load(f)

# Create a DataFrame
df = pd.json_normalize(data)

# Extract the required columns
df = df[['symbol', 'name', 'sector', 'financials.market_cap', 'financials.shares', 'financials.price', 'financials.EPS', 'financials.Sales']]

# Rename the columns for better readability
df.columns = ['symbol', 'name', 'sector', 'market_cap', 'shares', 'price', 'EPS', 'Sales']

# Ensure EPS and Sales are lists of strings
df['EPS'] = df['EPS'].apply(lambda x: x if isinstance(x, list) else [])
df['Sales'] = df['Sales'].apply(lambda x: x if isinstance(x, list) else [])

# Add current_eps column
df['current_eps'] = df['EPS'].apply(lambda x: parse_value(x[0]) if x else 0.0)

# Calculate CAGR for EPS and Sales with reversed lists
df['EPS_CAGR'] = df['EPS'].apply(lambda x: calculate_cagr([parse_value(i) for i in reversed(x)]))
df['Sales_CAGR'] = df['Sales'].apply(lambda x: calculate_cagr([parse_value(i) for i in reversed(x)]))

# Sort the DataFrame by highest values for EPS CAGR
df = df.sort_values(by='EPS_CAGR', ascending=False)

# Save the DataFrame to a CSV file
csv_output_path = 'analysis/cagr_analysis.csv'
df.to_csv(csv_output_path, index=False)

print(f"Data saved to {csv_output_path}")