import pandas
import datetime
import typing

from enum import Enum
import utils

from models import StockPrices



class Rebalance(Enum):
   EOM = 'EOM'
   NONE = "NONE"


prices = StockPrices('prices.csv')


class Position(object):

   def __init__(self, ticker: str, shares: float=None, dollars: float=None):
      self.shares = None
      self.dollars = None

      if shares is not None and dollars is not None:
         raise Exception("can't specify both shares and dollars")
      elif shares is not None:
         self.shares = shares
      elif dollars is not None:
         self.dollars = dollars
      else:
         raise Exception("must specify shares or dollars")

      self.ticker = ticker
   

class Portfolio(object):

   def __init__(self, name: str, positions: typing.List[Position], rebalance=Rebalance.NONE):
      self.name = name
      self.positions = positions
      self.rebalance = rebalance

   def calc_daily_returns(self, date_begin: datetime.date, date_end: datetime.date) -> pandas.DataFrame:
      
      dates = prices.get_trading_dates(date_begin, date_end)

      returns = []
      prev_date = None

      initial_dollars = 0

      allocations = {}
      prev_prices = {}

      for date in sorted(dates):
         if prev_date is None:
            # we buy in 
            for position in self.positions:
               price = prices.get_px(position.ticker, date)
               dollars = (price * position.shares if position.shares is not None else position.dollars)
               initial_dollars += dollars
               allocations[position.ticker] = dollars
               prev_prices[position.ticker] = price
            returns.append(None)
         else:
            
            dollars_prev = sum(allocations.values())
            
            for position in self.positions:
               price = prices.get_px(position.ticker, date)
               allocations[position.ticker] = allocations[position.ticker] * price / prev_prices[position.ticker]
               prev_prices[position.ticker] = price
            
            dollars_curr = sum(allocations.values())
            returns.append((dollars_curr - dollars_prev) / dollars_prev)

            if self.rebalance == Rebalance.NONE:
               pass  # do nothing
            elif self.rebalance == Rebalance.EOM:
               if prices.is_eom(date):
                  for ticker in allocations.keys():
                     allocations[ticker] = dollars_curr / len(allocations)

         prev_date = date

      # cut off the first date because there's no return
      return pandas.DataFrame({'Date': list(sorted(dates)), self.name: returns}).iloc[1:]
   

   def calc_total_annualized_return(self, date_begin: datetime.date, date_end: datetime.date) -> float:

      returns = self.calc_daily_returns(date_begin, date_end)
      total = 1
      for r in returns[self.name]:
         total *= (1 + r)
      total -= 1
      annualized = utils.annualize(total, (date_end - date_begin).days)
      return annualized
