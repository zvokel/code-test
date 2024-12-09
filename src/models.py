import pandas
import typing
import datetime
import utils


'''
   here's the interface for getting close prices and returns
'''
class StockPrices(object):

   def __init__(self, source: str, names: typing.List=None):

      prices = pandas.read_csv(source)
      
      if names:
         prices = prices[names]
      
      prices['Date'] = pandas.to_datetime(prices['Date'])

      self._prices = prices

   def get_px(self, ticker: str, date: datetime.date) -> float:      
      date = pandas.to_datetime(date)  # i hate this
      # this is dangerous if you ask for something that doesn't exist, 
      # but let's go with it for now
      return float(self._prices.loc[self._prices['Date'] == date][ticker])

   def get_return(self, ticker: str, date_begin: datetime.date, date_end: datetime.date) -> float:

      px_begin = self.get_px(ticker, date_begin)
      px_end = self.get_px(ticker, date_end)

      return (px_end - px_begin) / px_begin

   def get_annualized_return(self, ticker: str, date_begin: datetime.date, date_end: datetime.date) -> float:

      pct = self.get_return(ticker, date_begin, date_end)
      days = (date_end - date_begin).days

      return utils.annualize(pct, days)
      
   def get_trading_dates(self, date_begin: datetime.date, date_end: datetime.date) -> typing.List[datetime.date]: 

      return list(filter(lambda x: (x >= date_begin and x <= date_end), [y.date() for y in self._prices['Date']]))

   def get_start_trading_date(self, date: datetime.date) -> datetime.date:
      date = pandas.to_datetime(date)
      dates = self._prices.loc[self._prices['Date'] >= pandas.to_datetime(date)]
      if len(dates):
         return dates['Date'].iloc[0].date()
      else:
         return None         

   def get_end_trading_date(self, date:datetime.date) -> datetime.date:
      date = pandas.to_datetime(date)
      dates = self._prices.loc[self._prices['Date'] <= pandas.to_datetime(date)]
      if len(dates):
         return dates['Date'].iloc[0].date()
      else:
         return None         


   def is_eom(self, date: datetime.date):
      date = pandas.to_datetime(date)  # i hate this
      return self._prices.loc[self._prices['Date'] == date]['EndOfMonth'].iloc[0]




