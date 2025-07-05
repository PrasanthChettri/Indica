import pandas as pd
import json
from io import StringIO

# Original dictionary (shortened keys for demo; replace with your full dict)
data = {
    'ticker': 'TATAMOTORS.NS',
    'history': '2024-09-02    1040.40\n2024-09-09     983.64\n2024-09-16     962.57\n2025-06-30     683.80',
    'macd_data': '            MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9\n2025-06-30        -23.88          13.27         -37.15',
    'rsi_data': '45.1',
    'news_data': "Here's an analysis of the recent announcements...",
    'text': '''The stock will likely go down tomorrow...
```json
{
  "prediction": "The stock will likely go down tomorrow because the recent announcement of significant declines in Q1 FY26 Commercial and Passenger Vehicle sales is a strong negative fundamental signal, which is expected to lead to an immediate negative market reaction, overriding any minor positive technical indicators.",
  "sentiment": "sell",
  "news_impact": "The significant decline in Q1 FY26 Commercial and Passenger Vehicle sales is a strong negative fundamental signal, likely leading to an immediate negative market reaction."
}
```'''
}

# --- Extract and parse fields ---

# 1. Ticker
ticker = data['ticker']

# 2. Parse 'history' as a pandas Series
history = pd.read_csv(StringIO(data['history']), sep="\s+", header=None, names=["Date", "Close"], index_col=0)
history.index = pd.to_datetime(history.index)

# 3. Parse 'macd_data' as a pandas DataFrame
macd_df = pd.read_csv(StringIO(data['macd_data']), delim_whitespace=True, index_col=0)
macd_df.index = pd.to_datetime(macd_df.index)

# 4. Parse 'rsi_data' as float
rsi = float(data['rsi_data'])

# 5. News data (string)
news = data['news_data']

# 6. Extract embedded JSON from 'text' field
import re
text_body = data['text']
json_match = re.search(r"```json\s+(.*?)\s+```", text_body, re.DOTALL)
if json_match:
    prediction_data = json.loads(json_match.group(1))
else:
    prediction_data = {}

# --- Output ---
print("Ticker:", ticker)
print("\nHistory (last 2 rows):\n", history.tail(2))
print("\nMACD Data:\n", macd_df)
print("\nRSI:", rsi)
print("\nPrediction JSON:")
print(json.dumps(prediction_data, indent=2))

