import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-white')
import yfinance as yf

class StockTrading:

    def __init__(self,comp,invest):
        self.comp = comp
        self.invest = invest

    def stock_trend(self,start_date,end_date):
        closing_price = yf.download(self.comp,start=start_date,end=end_date).loc[:, 'Adj Close']
        plt.figure(figsize=(10, 6))
        closing_price.plot(title='Trend')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()

    def ma_crossover(self,start_date,end_date,period):
        short_window, long_window = 50, 200
        stockdata_df = yf.download(self.comp,start=start_date,end=end_date)
        short_term = stockdata_df['Adj Close'].rolling(window=short_window).mean()
        long_term = stockdata_df['Adj Close'].rolling(window=long_window).mean()
        adj_closing = stockdata_df.loc[:, 'Adj Close']
        initial_capital = self.invest
        capital = initial_capital
        flexible = 0.05 * capital
        capital -= flexible
        no_of_shares = flexible // adj_closing.iloc[0]
        flexible = 0
        sa_stores = []
        portfolio_value = []
        for s, l, p in zip(short_term, long_term, adj_closing):
            if pd.notna(s) and pd.notna(l):
                if s > l:
                    if flexible != 0:
                        no_of_shares += flexible // p
                        flexible = 0
                    else:
                        buy_amount = 0.9 * capital
                        no_of_shares += buy_amount // p
                        capital -= buy_amount
                else:
                    if sa_stores and (0.95 * sa_stores[-1] > s):
                        sell_shares = 0.9 * no_of_shares
                        flexible += sell_shares * p
                        no_of_shares -= sell_shares
                sa_stores.append(s)
            current_value = capital + flexible + (no_of_shares * p)
            portfolio_value.append(current_value)
        final_portfolio_value = capital + flexible + (no_of_shares * adj_closing.iloc[-1])
        ror = ((final_portfolio_value - initial_capital) / initial_capital) * 100
        cagr = (((final_portfolio_value / initial_capital) ** (1 / period)) - 1) * 100
        print("Moving Average Crossover")
        print(f"Final Portfolio Value: ${final_portfolio_value:.2f}")
        print(f"Rate of Return: {round(ror)}%")
        print(f"Annualised Average Return: {round(cagr)}%")
        portfolio_value_series = pd.Series(portfolio_value, index=stockdata_df.index)
        fig, ax = plt.subplots()
        ax.plot(short_term, label='Short-term MA')
        ax.plot(long_term, label='Long-term MA')
        ax.plot(adj_closing, label='Stock')
        ax.set_xlabel('Dates')
        ax.set_ylabel('Price')
        ax.set_title('Moving Averages')
        ax.legend()
        plt.figure(figsize=(10, 6))
        portfolio_value_series.plot(title='Moving Average Crossover')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.show()

    def mean_reversion(self,start_date,end_date,period,timeframe):
        window = timeframe
        listed = yf.download(self.comp, start=start_date, end=end_date)
        term = listed['Adj Close'].rolling(window=window).mean()
        rolling_std = listed['Adj Close'].rolling(window=window).std()
        closing = listed['Adj Close']
        money = self.invest
        money_available = money
        ready_money = 0.5 * money_available
        money_available -= ready_money
        total_shares = ready_money // closing.iloc[0]
        ready_money = 0
        portfolio_total = []
        for m, x, y in zip(term, rolling_std, closing):
            if pd.notna(x):
                if y < (m - 2 * x):
                    if ready_money != 0:
                        total_shares += ready_money // y
                        ready_money = 0
                    else:
                        buyer = 0.9 * money_available
                        total_shares += buyer // y
                        money_available -= buyer
                elif y > (m + 2 * x):
                    sale_of_shares = 0.9 * total_shares
                    ready_money += sale_of_shares * y
                    total_shares -= sale_of_shares
            current_money = money_available + ready_money + (total_shares * y)
            portfolio_total.append(current_money)
        total_portfolio_value = money_available + ready_money + (total_shares * closing.iloc[-1])
        r_of_r = ((total_portfolio_value - money) / money) * 100
        cag_return = (((total_portfolio_value / money) ** (1/period)) - 1) * 100
        print("Mean Reversion")
        print(f"Final Portfolio Value: ${total_portfolio_value:.2f}")
        print(f"Rate of Return: {round(r_of_r)}%")
        print(f"Annualised Average Return: {round(cag_return)}%")
        portfolio_value = pd.Series(portfolio_total, index=listed.index)
        plt.figure(figsize=(10, 6))
        portfolio_value.plot(title='Mean Reversion')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.show()

    def momentum_strategies(self,start_date,end_date,period,timeframe,bench):
        stock_price = yf.download(self.comp, start=start_date, end=end_date)['Adj Close']
        benchmark = yf.download(bench, start=start_date, end=end_date)['Adj Close']
        roc_st = stock_price.pct_change(periods=timeframe)
        roc_be = benchmark.pct_change(periods=timeframe)
        cash = self.invest
        cash_available = cash
        ready_cash = 0.5 * cash_available
        cash_available -= ready_cash
        all_shares = ready_cash // stock_price.iloc[0]
        ready_cash = 0
        portfolio_amount = []
        for x, y, m in zip(roc_st, roc_be, stock_price):
            if pd.notna(x) and pd.notna(y):
                rs = x/y
                if rs > 1 and x > 0.05:
                    if ready_cash != 0:
                        all_shares += ready_cash // m
                        ready_cash = 0
                    else:
                        buy = 0.9 * cash_available
                        all_shares += buy // m
                        cash_available -= buy
                elif rs < 1 and x < (-0.05):
                    sell_shares = 0.9 * all_shares
                    ready_cash += sell_shares * m
                    all_shares -= sell_shares
            current_cash = cash_available + ready_cash + (all_shares * m)
            portfolio_amount.append(current_cash)
        total_portfolio_amount = cash_available + ready_cash + (all_shares * stock_price.iloc[-1])
        rate_of_r = ((total_portfolio_amount - cash) / cash) * 100
        c_a_g_return = (((total_portfolio_amount / cash) ** (1 / period)) - 1) * 100
        print("Momentum Strategies")
        print(f"Final Portfolio Value: ${total_portfolio_amount:.2f}")
        print(f"Rate of Return: {round(rate_of_r)}%")
        print(f"Annualised Average Return: {round(c_a_g_return)}%")
        portfolio_value = pd.Series(portfolio_amount, index=yf.download(self.comp,start=start_date,end=end_date).index)
        plt.figure(figsize=(10, 6))
        portfolio_value.plot(title='Momentum Strategies')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.show()

trader = StockTrading("AAPL", 10000)
trader.stock_trend("2019-08-01", "2024-08-01")
trader.ma_crossover("2019-08-01", "2024-08-01", 5)
trader.mean_reversion("2024-02-01", "2024-08-01", 0.5, 100)
trader.momentum_strategies("2021-08-01", "2024-08-01", 3, 63, "^GSPC")