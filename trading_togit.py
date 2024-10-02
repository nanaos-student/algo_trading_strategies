import pandas as pd
import matplotlib.pyplot as plt
# Set the style for the plots
plt.style.use('seaborn-v0_8-white')
# Import the yfinance library for downloading stock data
import yfinance as yf


class StockTrading:
    def __init__(self, comp, invest):
        # Initialize the StockTrading class with company ticker and investment amount
        self.comp = comp
        self.invest = invest

    def stock_trend(self, start_date, end_date):
        # Download the adjusted closing prices for the given company and date range
        closing_price = yf.download(self.comp, start=start_date, end=end_date).loc[:, 'Adj Close']
        # Plot the closing prices
        plt.figure(figsize=(10, 6))
        closing_price.plot(title='Trend')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()

    def returns_calculation(self, final_investment, stocks, stock_price, init_investment, time, name, port_overtime,
                            starting, ending):
        # Calculate the total portfolio value
        total_portfolio_value = final_investment + (stocks * stock_price)
        # Calculate the rate of return (RoR)
        ror = ((total_portfolio_value - init_investment) / init_investment) * 100
        # Calculate the compound annual growth rate (CAGR)
        cag_return = (((total_portfolio_value / init_investment) ** (1 / time)) - 1) * 100
        # Print the results
        print(name)
        print(f"Final Portfolio Value: ${total_portfolio_value:.2f}")
        print(f"Rate of Return: {round(ror)}%")
        print(f"Annualised Average Return: {round(cag_return)}%")
        # Create a pandas Series for the portfolio value over time
        portfolio_value = pd.Series(port_overtime, index=yf.download(self.comp, start=starting, end=ending).index)
        # Plot the portfolio value over time
        plt.figure(figsize=(10, 6))
        portfolio_value.plot(title=name)
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.show()

    def ma_crossover(self, start_date, end_date, period):
        # Define the short and long window periods for moving averages
        short_window, long_window = 50, 200
        # Download stock data for the given company and date range
        stockdata_df = yf.download(self.comp, start=start_date, end=end_date)
        # Calculate short-term and long-term moving averages
        short_term = stockdata_df['Adj Close'].rolling(window=short_window).mean()
        long_term = stockdata_df['Adj Close'].rolling(window=long_window).mean()
        adj_closing = stockdata_df['Adj Close']
        # Initialise investment variables
        initial_capital = self.invest
        capital = initial_capital
        flexible = capital
        capital -= flexible
        no_of_shares = flexible // adj_closing.iloc[0]
        flexible = 0
        portfolio_value = []
        entry_price = adj_closing.iloc[0]  # Initial entry price
        # Iterate over the moving averages and adjusted closing prices
        for s, l, p in zip(short_term, long_term, adj_closing):
            if pd.notna(s) and pd.notna(l):
                if s > l:  # Golden Cross (buy signal)
                    buy_amount = capital
                    no_of_shares += buy_amount // p
                    capital -= buy_amount
                    entry_price = p  # Update entry price on buy
                elif p > (0.8 * entry_price):  # Quick re-entry
                    no_of_shares += flexible // p
                    flexible = 0
                elif p < (0.9 * entry_price):  # Stop-Loss (partial sell)
                    sell_shares = 0.5 * no_of_shares
                    flexible += sell_shares * p
                    no_of_shares -= sell_shares
                elif s < l:  # Death Cross (full sell)
                    sell_shares = no_of_shares
                    capital += sell_shares * p
                    no_of_shares = 0  # Fully sell out
            # Calculate current portfolio value
            current_value = capital + flexible + (no_of_shares * p)
            portfolio_value.append(current_value)
        total = capital + flexible
        #Calculate final portfolio value, rate of return, and CAGR
        self.returns_calculation(total, no_of_shares, adj_closing.iloc[-1], initial_capital, period,"Moving Average Crossover", portfolio_value, start_date, end_date)

    def mean_reversion(self, start_date, end_date, period, timeframe):
        # Define the rolling window period for calculating moving averages and standard deviation
        window = timeframe
        # Download stock data for the given company and date range
        listed = yf.download(self.comp, start=start_date, end=end_date)
        # Calculate the rolling mean and standard deviation of the adjusted closing prices
        term = listed['Adj Close'].rolling(window=window).mean()  # Rolling mean
        rolling_std = listed['Adj Close'].rolling(window=window).std()  # Rolling std dev
        closing = listed['Adj Close']
        # Initialise investment variables
        money = self.invest
        money_available = money
        # Initial investment (50% of capital)
        total_shares = (0.5 * money_available) // closing.iloc[0]
        money_available -= total_shares * closing.iloc[0]
        # Portfolio tracking
        portfolio_total = []
        # Maximum position size (capping position size)
        max_position_size = 0.1 * money  # 10% of total capital as a max position
        # Iterate over the rolling mean, standard deviation, and closing prices
        for m, x, y in zip(term, rolling_std, closing):
            if pd.notna(x):
                # Position sizing with a cap to avoid overbuying
                position_size = min(0.03 * money, max_position_size) / (y - (m - 2 * x))
                # Buy signal (price below lower Bollinger Band)
                if y < (m - 2 * x) and money_available > 0:
                    shares_to_buy = position_size // y
                    total_shares += shares_to_buy
                    money_available -= shares_to_buy * y
                # Re-entry logic: Price between mean and lower band, limited buying
                elif y < m and y > (m - 2 * x) and money_available > 0:
                    reentry_position = min(0.01 * money, max_position_size) / (y - m)  # Smaller re-entry size
                    shares_to_buy = reentry_position // y
                    total_shares += shares_to_buy
                    money_available -= shares_to_buy * y
                # Partial selling at upper Bollinger Band (75% of total shares)
                elif y == (m + 2 * x) and total_shares > 0:
                    sale_of_shares = 0.75 * total_shares
                    money_available += sale_of_shares * y
                    total_shares -= sale_of_shares
                # Additional selling when price exceeds upper Bollinger Band by 10% (25% of remaining shares)
                elif y > (m + 2 * x) * 1.1 and total_shares > 0:
                    sale_of_shares = 0.25 * total_shares
                    money_available += sale_of_shares * y
                    total_shares -= sale_of_shares
            # Track portfolio value
            current_money = money_available + (total_shares * y)
            portfolio_total.append(current_money)
        #Calculate final portfolio value, rate of return, and CAGR
        self.returns_calculation(money_available, total_shares, closing.iloc[-1], money, period, "Mean Reversion", portfolio_total, start_date, end_date)

    def momentum_strategies(self, start_date, end_date, period, timeframe, bench):
        # Download stock and benchmark data for the given date range
        stock_price = yf.download(self.comp, start=start_date, end=end_date)['Adj Close']
        benchmark = yf.download(bench, start=start_date, end=end_date)['Adj Close']
        # Calculate the rate of change (ROC) for the stock and benchmark
        roc_st = stock_price.pct_change(periods=timeframe)
        roc_be = benchmark.pct_change(periods=timeframe)
        # Initialise investment variables
        cash = self.invest
        cash_available = cash
        all_shares = cash_available // stock_price.iloc[0]
        cash_available -= all_shares * stock_price.iloc[0]
        # Set initial take-profit and stop-loss levels
        takeprofit_price = stock_price.iloc[0] * (1 + 0.15)  # Initial take-profit level
        stoploss_price = stock_price.iloc[0] * (1 - 0.05)  # Initial stop-loss level
        risk = 0.05  # Example: risk 5% of total capital per trade
        # Track portfolio value over time
        portfolio_amount = []
        # Iterate over the ROC and stock prices
        for x, y, m in zip(roc_st, roc_be, stock_price):
            if pd.notna(x) and pd.notna(y):
                rs = x / y  # Relative strength
                # Buy Signal
                if rs > 1 and x > 0.05:  # Momentum buy signal
                    stoploss_price = m * (1 - 0.05)
                    position_size = (risk * cash) / (m - stoploss_price)  # Position sizing based on stop-loss
                    buy_amount = cash_available if cash_available < position_size else position_size
                    shares_to_buy = buy_amount // m
                    all_shares += shares_to_buy
                    cash_available -= shares_to_buy * m
                    # Update take-profit after buying
                    takeprofit_price = m * (1 + 0.15)
                # Take-Profit Trigger
                elif m >= takeprofit_price:  # If stock hits take-profit price
                    sell_shares = 0.5 * all_shares  # Partial selling
                    cash_available += sell_shares * m
                    all_shares -= sell_shares
                    # Recalculate take-profit and stop-loss after partial sell
                    takeprofit_price = m * (1 + 0.15)
                    stoploss_price = m * (1 - 0.05)
                # Stop-Loss or Underperformance Trigger
                elif (rs < 1 and x < -0.05) or m <= stoploss_price:  # Full exit condition
                    sell_shares = all_shares
                    cash_available += sell_shares * m
                    all_shares = 0  # Full exit
                # Recalculate stop-loss and take-profit after full or partial exits
                takeprofit_price = m * (1 + 0.15)
                stoploss_price = m * (1 - 0.05)
            # Calculate current portfolio value and append to portfolio history
            current_cash = cash_available + (all_shares * m)
            portfolio_amount.append(current_cash)
        #Calculate final portfolio value, rate of return, and CAGR
        self.returns_calculation(cash_available, all_shares, stock_price.iloc[-1], cash, period,"Momentum Strategies", portfolio_amount, start_date, end_date)


#Create an instance of the StockTrading class for Apple Inc. with an investment of $10,000
trader = StockTrading("AAPL", 10000)

#Plot the stock trend for Apple Inc. from August 1, 2019, to August 1, 2024
trader.stock_trend("2019-08-01", "2024-08-01")
#Test the Moving Average Crossover strategy
trader.ma_crossover("2022-08-01", "2024-08-01", 2)
#Test the Mean Reversion strategy
trader.mean_reversion("2024-03-01", "2024-09-01", 0.5, 100)
#Test the Momentum Strategies
trader.momentum_strategies("2021-08-01", "2024-08-01", 3, 63, "^GSPC")
