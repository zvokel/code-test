# Preamble

Here's the code for the ANONYMOUS coding challenge I was given.  The repo is public at the moment (but does not include the challenge instructions, only the code I wrote to solve it) but I'm happy to make it private once it has been reviewed.

Let's get the model outputs out of the way:

The correlation between the equal-share and equal weight portfolio is: 0.9717702699879794
The correlation between the equal-share and EOM rebalanced portfolio is: 0.9810334332520371
The correlation between the equal weight and EOM rebalanced portfolio is: 0.9952871007830019

Total (annualized) return for equal-share portfolio is 92.98%
Total (annualized) return for equal weight portfolio is 115.29%
Total (annualized) return for EOM rebalanced portfolio is 113.02%

I've included `output.csv` with the daily return vectors for the three portfolios.  I've also included a `requirements.txt` if you want to run the whole thing yourself.  I'm using Python 3.12.6.

One note: the time period was given as 12/31/2022 to 12/31/2023, neither of which are trading days.  For the purposes of running the analysis the positions were entered at the close on the first trading day after 12/31/2022 and evaluated on the final trading day before 12/31/2023.  This makes a difference in the annualized total return value, since the period is slightly less than a year.


# ETL

This part was pretty easy; I just used `yfinance` to get the prices for the seven stocks.  I used the adjusted close because I didn't want to muck around with splits or dividends; this was the only series that was saved.


# Data Source

I made a class that holds all of the data and has methods to get prices and returns.  I also added a method to get whether a date is the end of the month.  This is a little hacky and probably doesn't belong here, but I didn't want to make a trading calendar class.  In a real application, I would.

It's been a minute since I've worked a lot with Pandas and its timestamps, so some of this code might be a little ugly.  The doc said to design this to work with 20K data points per day.  That doesn't seem like a lot of data and I think the design should be fine?  Where there are janky things in the code I try to note them.


# Portfolio Modeling

I made two classes, `Portfolio` and `Position`.  A `Position` represents a ticker and quantity (either in shares or dollars).  A `Portfolio` consists of a collection of `Position` objects and a rebalance method, represented as a member of the `Rebalance` enum.  To get the returns for a portfolio, give it start and end dates.  Is this the only way to model this?  No, but it's the one I chose, and for this use case it works pretty nicely.


# Calculations

The file `script.py` builds the portfolios, gets the returns, and prints out things like the total return and correlations.

