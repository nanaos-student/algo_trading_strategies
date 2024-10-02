Stock Trading Strategies Implementation

This Python project implements three popular stock trading strategies: Moving Average Crossover, Mean Reversion, and Momentum Strategies. It also includes basic risk management techniques such as stop-losses, take-profits, partial selling, and position sizing etc.

Features
1. Moving Average Crossover Strategy:
   - Uses 50-day and 200-day moving averages to generate buy and sell signals.
   - Buy signal (Golden Cross): When the 50-day moving average crosses above the 200-day moving average.
   - Sell signal (Death Cross): When the 50-day moving average crosses below the 200-day moving average.
   - Includes stop-loss and quick re-entry logic.

2. Mean Reversion Strategy:
   - Uses Bollinger Bands to identify overbought and oversold conditions.
   - Buy when the price drops below the lower Bollinger Band.
   - Sell 75% of the position when the price reaches the upper Bollinger Band and an additional 25% when the price exceeds 10% above the upper band.

3. Momentum Strategy:
   - Uses Rate of Change (ROC) and Relative Strength (RS) compared to a benchmark.
   - Buy when the stock has positive momentum and is outperforming the benchmark.
   - Partial selling when the stock hits a take-profit level.
   - Full exit on stop-loss or underperformance.

Requirements
- Python 3.7+
- yfinance: For downloading historical stock data.
- pandas: For data manipulation.
- matplotlib: For plotting stock trends and portfolio performance.

Usage

1. Initialise the Trading System:
   Create an instance of the `StockTrading` class by specifying the stock ticker and the initial investment.
2. Stock Trend Plotting:
   Plot the trend of a stock between two dates.
3. Moving Average Crossover Strategy:
   Test the moving average crossover strategy for a specified time-period.
4. Mean Reversion Strategy:
   Test the mean reversion strategy for a specified time-period with a set-day window.
5. Momentum Strategy:
   Test the momentum strategy for a specified time-period, using a set trading days for the momentum calculation, with the S&P 500 as a benchmark.

Output

For each strategy, the code will:
- Display the stock's trend.
- Plot the portfolio's value over time.
- Output the final portfolio value, rate of return (RoR), and compound annual growth rate (CAGR).

Risk Management

- Stop-Loss: Automatically sell portions or the entire position if the stock price drops below a certain percentage.
- Take-Profit / Risk-to-Reward: Sell part of the position when a profit target is reached.
- Position Sizing: Adjust the number of shares purchased based on the risk level (stop-loss distance) and capital available.
