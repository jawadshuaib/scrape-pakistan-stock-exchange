/**
 * This script calculates the intrinsic value of stocks based on their share price, EPS, and growth rate.
 * It fetches data from an external API and writes the intrinsic value to a specific cell in Google Sheets.
 *
 * The steps involved are:
 * 1. Iterate through each row of the sheet.
 * 2. Skip rows with missing or insufficient data.
 * 3. Define parameters for the valuation calculation.
 * 4. Construct the URL for the API request.
 * 5. Make an HTTP GET request to the API.
 * 6. Parse the JSON response to extract the intrinsic value.
 * 7. Write the intrinsic value to the corresponding cell in the sheet.
 * 8. Log any errors encountered during the process.
 *
 * How to use this script in Google Sheets:
 * 1. Open your Google Sheet.
 * 2. Go to Extensions > Apps Script.
 * 3. Delete any code in the script editor and paste this script.
 * 4. Save the script with a name, e.g., "Stock Valuation Script".
 * 5. Close the script editor.
 * 6. In your Google Sheet, go to Extensions > Macros > Import and select the function you want to run.
 * 7. Run the macro to calculate and populate the intrinsic values.
 */

function getStockValue() {
	var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
	var lastRow = sheet.getLastRow();

	// Loop through each row starting from the second row
	for (var i = 2; i <= lastRow; i++) {
		var sharePrice = sheet.getRange('F' + i).getValue();
		var eps = sheet.getRange('I' + i).getValue();
		var growthRate = sheet.getRange('J' + i).getValue();
		growthRate = growthRate * 100;

		// If any of the required values are empty, skip the row
		if (sharePrice === '' || eps === '' || growthRate === '') {
			continue;
		}

		if (growthRate < 10) {
			continue;
		}

		// Define the other parameters
		var terminalGrowthRate = 3;
		var discountRate = 15;
		var marginOfSafety = 50;

		// Construct the URL
		var url = `https://stock-valuation.netlify.app/.netlify/functions/calculateEPS?sharePrice=${sharePrice}&eps=${eps}&growthRate=${growthRate}&terminalGrowthRate=${terminalGrowthRate}&discountRate=${discountRate}&marginOfSafety=${marginOfSafety}`;

		try {
			// Make the HTTP GET request
			var response = UrlFetchApp.fetch(url);
			var json = JSON.parse(response.getContentText());

			// Get the intrinsic value from the response
			var intrinsicValue = json.intrinsic_value;

			// Write the intrinsic value to the specific cell in column L
			sheet.getRange('L' + i).setValue(intrinsicValue);
		} catch (e) {
			Logger.log('Error fetching data for row ' + i + ': ' + e);
		}
	}
}
