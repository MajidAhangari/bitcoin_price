Bitcoin Price Tracker README
Overview
This project is a Python script designed to track and log both live and historical Bitcoin prices. The script utilizes the `ccxt` library to fetch live Bitcoin prices from the Binance exchange and the `yfinance` library to retrieve historical data from Yahoo Finance. The data is saved into an Excel file and updated every minute.
Prerequisites
Before running the script, ensure you have the following dependencies installed:
•	- Python 3.x
- `ccxt` (for accessing cryptocurrency exchange data)
- `yfinance` (for downloading historical financial data)
- `pandas` (for data manipulation and storage)
- `openpyxl` (for Excel file operations)
- `pytz` (for timezone management)
You can install the required packages using pip:
pip install ccxt yfinance pandas openpyxl pytz
Features
•	- **Live Price Fetching:** The script fetches the live price of Bitcoin in USD (BTC/USDT) from Binance every minute.
- **Historical Data Retrieval:** It retrieves historical data for Bitcoin across various timeframes (e.g., daily, hourly, minute-wise) using Yahoo Finance.
- **Excel File Storage:** Both live and historical data are saved into an Excel file (`bitcoin_data_utc.xlsx`). The file is updated every minute with the latest price and historical data.
- **Timezone Handling:** All data is stored in UTC (Coordinated Universal Time) for consistency.
Usage
1. **Initial Data Fetching:**
   - The script first fetches historical Bitcoin data for various timeframes and stores it in an Excel file.
   - Timeframes include daily, hourly, minute-wise, weekly, and monthly data over various periods (e.g., 5 years, 1 month).

2. **Continuous Updating:**
   - The script enters an infinite loop where it:
     - Fetches the current live price of Bitcoin.
     - Retrieves the latest historical data for each timeframe.
     - Updates the Excel file with the latest live price and historical data.
   - The Excel file is updated every minute.

3. **Excel File Structure:**
   - The Excel file (`bitcoin_data_utc.xlsx`) contains multiple sheets:
     - **Historical Data:** Separate sheets for each timeframe (e.g., `Historical 1d`, `Historical 1h`).
     - **Live Price:** A sheet (`Live Price`) that logs the Bitcoin price every minute with a timestamp.
Customization
•	- **Timeframes and Periods:** You can adjust the timeframes and periods for historical data by modifying the `timeframes` dictionary.
- **File Path:** The path to the Excel file can be modified by changing the `file_path` variable.
Limitations
•	- The script is designed to run indefinitely. Ensure you have sufficient system resources and manage the process manually if needed.
- Network errors or API limitations may impact data retrieval, especially during extended use.
How to Run
Simply execute the script in your terminal:
python bitcoin_price_tracker.py
The script will start fetching and logging Bitcoin prices immediately. You can monitor its output directly in the terminal.
Conclusion
This script provides a straightforward solution for tracking Bitcoin prices and storing the data in a structured format. It's ideal for anyone interested in analyzing Bitcoin's price movements over time.
---

