# Forecasting price time-series based on historical values and classifying a buy/sell action using supervised machine learning 
Author: Terence Yep

![Image of stock chart](img/candle-stick-graph-stock.jpg?raw=true "Image of stock chart")
<br>
Source: Getty Images

## Introduction
When evaluating the price of a business/stock, there are two schools of thought: [Fundamental Analysis](https://www.investopedia.com/articles/trading/06/fundamentalapproach.asp), which measures the stock's intrinsic value by studying the economy, industry the company operates in and the company itself. And [technical analysis](https://www.investopedia.com/terms/t/technicalanalysis.asp), which evaluates trading opportunities from analyzing price movement and volume. Apart from that, we also need to take into consideration how traders will react to macroeconomic trends, financial news, market anouncements, analyst forecasts to name a few. 

## Problem statement
Daily stock price data is in essence a time-series, where a security’s price, over a specified period of time with data points recorded at regular intervals. We can then predict future activity based on the patterns associated to the time-series. This relates to trend analysis, cyclical fluctuation analysis, and issues of seasonality.
So how does one go about predicting the price for a given security? Is it possible to leverage machine learning using price data alone to forecast tomorrow's price? How about six months from now? And can we accurately recommend buy or sell actions to retain our gains prior to a major downturn?

We will attempt to answer those questions by:

- Investigating various machine learning models to forecast the price of Microsoft (MSFT)
- Recommend a buy/sell action based on predictions.  

### Who Cares? 
This type of problem is typically encountered by Financial institutions: 

- Fund/Portfolio Managers
- Investment Analysts 
- Retail investors 

But beyond financial institutions, the method can virtually be applied to problems that involve time-series. For eg, hardware failure due to wear and tear, weather pattern prediction to name some applications that currently use similar methods to forecast trends. 

### Data sources

* Yahoo Finance api 
* Quandl api 

### Visualization 

{% include img/candlestick-chart.html %}
Fig I. Interactive candlestick chart of MSFT over 3 years. Overlayed 50, 100 and 200 day moving average plots.   

### Limitations

As mentioned earlier, we're trying to forecast the price based on historical price data. 

- Biases
    * Buy/sell labels were generated based on user's understanding of investment strategies. 

- Incomplete information
    * Macro trends were not considered. 
    * Financials of company not considered.
    * News not considered. 
 



