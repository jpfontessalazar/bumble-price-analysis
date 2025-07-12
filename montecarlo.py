import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ticker_symbol = input("Enter the stock ticker symbol: ").upper()

# download historical data
ticker = yf.Ticker(ticker_symbol)
data = ticker.history(period="1y")  # last 1 year of data
print(data.head())

# calculate daily returns, mean and standard deviation
data['Daily_Return'] = data['Close'].pct_change()
mu = data['Daily_Return'].mean()
sigma = data['Daily_Return'].std()

print(f"Mean Daily Return: {mu:.4f}")
print(f"Daily Volatility: {sigma:.4f}")

days = 252  # 1 año bursátil
simulations = 10000  # número de escenarios

last_price = data['Close'].iloc[-1]
simulation_df = pd.DataFrame()

for x in range(simulations):
    price_series = [last_price]
    for d in range(days):
        price = price_series[-1] * np.exp((mu - 0.5 * sigma**2) + sigma * np.random.normal())
        price_series.append(price) 
    simulation_df[x] = price_series

import matplotlib.pyplot as plt

plt.figure(figsize=(15,7))
plt.plot(simulation_df)
plt.title(f"Monte Carlo Simulation: {ticker_symbol} - {simulations} runs, {days} days")
plt.xlabel('Days')
plt.ylabel('Price')
plt.show()

# Últimos precios simulados
ending_prices = simulation_df.iloc[-1, :]

# Percentiles
p5 = np.percentile(ending_prices, 5)
p25 = np.percentile(ending_prices, 25)
p50 = np.percentile(ending_prices, 50)
p75 = np.percentile(ending_prices, 75)
p95 = np.percentile(ending_prices, 95)

# Current price
current_price = data['Close'].iloc[-1]

# Expected return (usando mediana)
expected_return = (p50 / current_price - 1) * 100  # en %

# Volatilidad de precios finales
volatility = np.std(ending_prices) / current_price * 100  # en %

# Print resultados
print(f"\nMonte Carlo Simulation Results for {ticker_symbol}:")
print(f"Current Price: ${current_price:.2f}")
print(f"Median Price (P50): ${p50:.2f}")
print(f"Expected Return: {expected_return:.2f}%")
print(f"5th Percentile (worst case): ${p5:.2f}")
print(f"25th Percentile: ${p25:.2f}")
print(f"75th Percentile: ${p75:.2f}")
print(f"95th Percentile (best case): ${p95:.2f}")
print(f"Volatility of final prices: {volatility:.2f}%")

# Histograma de precios finales
plt.figure(figsize=(10,6))
plt.hist(ending_prices, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(p5, color='red', linestyle='dashed', linewidth=1.5, label='5th percentile')
plt.axvline(p25, color='orange', linestyle='dashed', linewidth=1.5, label='25th percentile')
plt.axvline(p50, color='black', linestyle='dashed', linewidth=1.5, label='Median (P50)')
plt.axvline(p75, color='green', linestyle='dashed', linewidth=1.5, label='75th percentile')
plt.axvline(p95, color='purple', linestyle='dashed', linewidth=1.5, label='95th percentile')
plt.title(f"Distribution of final simulated prices for {ticker_symbol}")
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.xlim(0, 20)  # ajusta el rango según tus precios reales
plt.legend()
plt.show()

