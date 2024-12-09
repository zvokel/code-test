import yfinance
import datetime
import pandas


def extract(tickers: str, start: datetime.date, end: datetime.date) -> pandas.DataFrame:

   # we fetch with a bit of a buffer on either end
   data = yfinance.download(tickers, start - datetime.timedelta(5), end + datetime.timedelta(5))

   return data

def transform(data: pandas.DataFrame, start: datetime.date, end: datetime.date) -> pandas.DataFrame:
   ''' 
      the transformation is:

      1. adding a field representing whether the date is the end of the month
      2. truncating the data to our start and end dates

      the reason we add the EOM field is as a bit of a hack to obviate the need
      for a trading calendar.  i'd make one if this were a real project, but 
      it's not so i'm not going to go through the trouble.
   '''

   # we're going to get false EOM values on the first and last rows in the df
   data['month'] = pandas.Series(data.index, index=data.index).apply(lambda x: x.month)
   data['EndOfMonth'] = (data['month'] != data['month'].shift(-1)) 

   # ...but it's okay because we're going to throw them away anyway
   data = data.loc[data.index >= pandas.to_datetime(start)]
   data = data.loc[data.index <= pandas.to_datetime(end)]

   # using the adjusted close to account for splits & dividends.
   # in the real world we'd want to save out more than this but in this case
   # it's all we're using, so it's all we save.
   prices = data['Adj Close'].reset_index()
   eom = data['EndOfMonth'].reset_index()

   prices['EndOfMonth'] = eom['EndOfMonth']

   return prices


def load(prices: pandas.DataFrame, destination: str) -> None:
   # XXX beware, this could cause a collision if there were a DATE ticker in here
   prices.to_csv(destination, index=False)


def etl(tickers, start, end, destination) -> None:
   data = extract(tickers, start, end)
   prices = transform(data, start, end)
   load(prices, destination)


if __name__ == '__main__':

   start = datetime.date(2022, 12, 31)  # not a trading day; first trading day after is 1/3/2023
   end = datetime.date(2023, 12, 31)  # not a trading day; last trading day before is 12/29/2023
   tickers = 'MSFT NVDA META GOOG TSLA AMZN AAPL'
   destination = 'prices.csv'

   etl(tickers, start, end, destination)
