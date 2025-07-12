import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# input ticker symbol
# Example: ticker_symbol = "AAPL" for Apple Inc.
ticker_symbol = input("Enter the stock ticker symbol: ").upper()

# download historical data
ticker = yf.Ticker(ticker_symbol)
data = ticker.history(period="1y")  # last 1 year of data
print(data.head())

# calculate moving averages
data['SMA_20'] = data['Close'].rolling(window=20).mean()
plt.figure(figsize=(14,7))
plt.plot(data.index, data['Close'], label='Close Price', color='blue')
plt.plot(data.index, data['SMA_20'], label='20-Day SMA', color='orange')
plt.title(f"{ticker_symbol} Stock Price and 20-Day SMA")
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
#plt.show()

#data['SMA_50'] = data['Close'].rolling(window=50).mean()
#plt.figure(figsize=(14,7))
#plt.plot(data.index, data['Close'], label='Close Price', color='blue')
#plt.plot(data.index, data['SMA_20'], label='50-Day SMA', color='orange')
#plt.title(f"{ticker_symbol} Stock Price and 50-Day SMA")
#plt.xlabel('Date')
#plt.ylabel('Price (USD)')
#plt.legend()
#plt.show()

#data['SMA_100'] = data['Close'].rolling(window=100).mean()
#plt.figure(figsize=(14,7))
#plt.plot(data.index, data['Close'], label='Close Price', color='blue')
#plt.plot(data.index, data['SMA_20'], label='100-Day SMA', color='orange')
#plt.title(f"{ticker_symbol} Stock Price and 100-Day SMA")
#plt.xlabel('Date')
#plt.ylabel('Price (USD)')
#plt.legend()
#plt.show()

# calculate exponential moving averages
data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
plt.figure(figsize=(14,7))
plt.plot(data.index, data['Close'], label='Close Price', color='blue')
plt.plot(data.index, data['SMA_20'], label='20-Day SMA', color='orange')
plt.plot(data.index, data['EMA_20'], label='20-Day EMA', color='green')
plt.title(f"{ticker_symbol} Stock Price and SMA & EMA 20")
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# calculate change in price
delta = data['Close'].diff()

# gain/loss
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

# relative strength index (RSI)
rs = gain / loss
data ['RSI'] = 100 - (100 / (1 + rs))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8), sharex=True)

# Gráfica 1: Precio + SMA + EMA
ax1.plot(data.index, data['Close'], label='Precio de Cierre')
ax1.plot(data.index, data['SMA_20'], label='SMA 20', color='orange')
ax1.plot(data.index, data['EMA_20'], label='EMA 20', color='green')
ax1.set_title(f'{ticker_symbol} - Precio, SMA & EMA')
ax1.legend()

# Gráfica 2: RSI
ax2.plot(data.index, data['RSI'], label='RSI 14 días', color='purple')
ax2.axhline(70, color='red', linestyle='--')  # sobrecompra
ax2.axhline(30, color='green', linestyle='--')  # sobreventa
ax2.set_title('RSI 14 días')
ax2.legend()

plt.show()

# Bollinger Bands
# SMA de 20 días (ya la tienes, pero la recalculamos para claridad)
data['SMA_20'] = data['Close'].rolling(window=20).mean()

# Desviación estándar de 20 días
data['STD_20'] = data['Close'].rolling(window=20).std()

# Bollinger Bands
data['Upper_Band'] = data['SMA_20'] + 2 * data['STD_20']
data['Lower_Band'] = data['SMA_20'] - 2 * data['STD_20']

plt.figure(figsize=(14,7))
plt.plot(data.index, data['Close'], label='Close Price', color='blue')
plt.plot(data.index, data['SMA_20'], label='20-Day SMA', color='orange')
plt.plot(data.index, data['Upper_Band'], label='Upper Band', color='green')
plt.plot(data.index, data['Lower_Band'], label='Lower Band', color='red')
plt.fill_between(data.index, data['Upper_Band'], data['Lower_Band'], color='lightgrey', alpha=0.3)
plt.title(f"{ticker_symbol} - Bollinger Bands")
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# MACD
data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
data['MACD'] = data['EMA_12'] - data['EMA_26']
data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

# Plotting MACD
fig, ax = plt.subplots(figsize=(14,7))

# Línea MACD
ax.plot(data.index, data['MACD'], label='MACD', color='blue')
# Línea de Señal
ax.plot(data.index, data['Signal_Line'], label='Signal Line', color='red')

# Histograma
hist = data['MACD'] - data['Signal_Line']
ax.bar(data.index, hist, color='grey', alpha=0.3, label='Histogram')

ax.set_title(f'{ticker_symbol} - MACD')
ax.legend()
plt.show()

