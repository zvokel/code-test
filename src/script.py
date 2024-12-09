import datetime
import pandas
import numpy as np

from analytics import Portfolio, Position, Rebalance



tickers = [
   'AAPL',
   'MSFT',
   'GOOG',
   'AMZN',
   'NVDA',
   'META',
   'TSLA',
]


def run_analysis(date_begin: datetime.date, date_end: datetime.date):

   one_share_positions = [Position(t, shares=1) for t in tickers]
   one_share_portfolio = Portfolio('one share', one_share_positions, rebalance=Rebalance.NONE)

   equal_weight_positions = [Position(t, dollars=1) for t in tickers]
   equal_weight_portfolio = Portfolio('equal weight', equal_weight_positions, rebalance=Rebalance.NONE)

   eom_rebalance_positions = [Position(t, dollars=1) for t in tickers]
   eom_rebalance_portfolio = Portfolio('rebalanced', eom_rebalance_positions, rebalance=Rebalance.EOM)

   equal_weight_returns = equal_weight_portfolio.calc_daily_returns(date_begin, date_end)
   one_share_returns = one_share_portfolio.calc_daily_returns(date_begin, date_end)
   eom_rebalance_returns = eom_rebalance_portfolio.calc_daily_returns(date_begin, date_end)

   all_returns = pandas.merge(equal_weight_returns, one_share_returns, how='outer', on='Date')
   all_returns = pandas.merge(all_returns, eom_rebalance_returns, how='outer', on='Date')

   all_returns.to_csv('output.csv', index=False)


   corr = np.corrcoef(all_returns['one share'], all_returns['rebalanced'])[0][1]

   print("The correlation between the equal-share and equal weight portfolio is: {0}".format(
      np.corrcoef(all_returns['one share'], all_returns['equal weight'])[0][1]
   ))
   print("The correlation between the equal-share and EOM rebalanced portfolio is: {0}".format(
      np.corrcoef(all_returns['one share'], all_returns['rebalanced'])[0][1]
   ))
   print("The correlation between the equal weight and EOM rebalanced portfolio is: {0}".format(
      np.corrcoef(all_returns['equal weight'], all_returns['rebalanced'])[0][1]
   ))

   print("Total (annualized) return for equal-share portfolio is {0:.2f}%".format(
      one_share_portfolio.calc_total_annualized_return(date_begin, date_end) * 100
   ))
   print("Total (annualized) return for equal weight portfolio is {0:.2f}%".format(
      equal_weight_portfolio.calc_total_annualized_return(date_begin, date_end) * 100
   ))
   print("Total (annualized) return for EOM rebalanced portfolio is {0:.2f}%".format(
      eom_rebalance_portfolio.calc_total_annualized_return(date_begin, date_end) * 100
   ))

   


if __name__ == '__main__':

   date_begin = datetime.date(2022, 12, 31)
   date_end = datetime.date(2023, 12, 31)

   run_analysis(date_begin, date_end)
