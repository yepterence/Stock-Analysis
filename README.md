# Forecasting price time-series based on historical values and classifying a buy/sell action using supervised machine learning 
Author: Terence Yep

![Image of stock chart](img/candle-stick-graph-stock.jpg?raw=true "Image of stock chart")
## Introduction
When evaluating the price of a business/stock, there are two schools of thought: [Fundamental Analysis](https://www.investopedia.com/articles/trading/06/fundamentalapproach.asp), which measures the stock's intrinsic value by studying the economy, industry the company operates in and the company itself. And [technical analysis](https://www.investopedia.com/terms/t/technicalanalysis.asp), which evaluates trading opportunities from analyzing price movement and volume. Apart from that, we also need to take into consideration how traders will react to macroeconomic trends, financial news, market anouncements, analyst forecasts to name a few. 

## Problem statement
So how does one go about predicting the price if we do want to perform technical analysis on a particular stock? 
Daily stock price data is in essence a time-series 

The objective of this project is two fold:

- Develop a model that forecasts price 
- Accurately predict a buy/sell action 

### Who Cares? 
This type of problem is typically encountered by Financial institutions: 

- Fund/Portfolio Managers
- Investment Analysts 
- Retail investors 

But beyond financial institutions, the method can virtually be applied to problems that involve time-series. For eg, hardware failure due to wear and tear, weather pattern prediction to name some applications that currently use similar methods to forecast trends. 

### Data sources

* Yahoo Finance api 
* Quandl api 

### Limitations

As mentioned earlier, we're trying to forecast the price based on historical price data. 

- Biases
    * Buy/sell labels were generated based on user's understanding of investment strategies. 
     
- Incomplete information
    * Macro trends were not considered. 
    * Financials of company not considered.
    * News not considered. 
 



