# Stock Analysis with LLM
## 1. Interactive Dashboard Features
- Real-time/Historical price visualization
- Multiple timeframes (Intraday, Daily, Weekly, Monthly)
- Multiple chart types (Candlestick, Line, OHLC)
- Indicator overlay options
- Stock comparison features
- Interactive controls for timeframe and indicator selection

## 2. Technical Indicators & Analysis

### A. Trend Indicators

#### Moving Averages (SMA/EMA)
- SMA: Simple average over a period
- EMA: Weighted average giving more importance to recent prices
- Common periods: 20, 50, 200 days
- Signals:
  * Golden Cross (50 MA crosses above 200 MA): Bullish
  * Death Cross (50 MA crosses below 200 MA): Bearish

#### MACD (Moving Average Convergence Divergence)
- Components: MACD line, Signal line, Histogram
- Default settings: (12, 26, 9)
- Signals:
  * MACD crosses above signal line: Buy
  * MACD crosses below signal line: Sell
  * Divergence patterns indicate potential reversals

### B. Momentum Indicators

#### RSI (Relative Strength Index)
- Measures speed and magnitude of price changes
- Range: 0-100
- Signals:
  * Above 70: Overbought
  * Below 30: Oversold
  * Divergence with price indicates potential reversal

#### Stochastic Oscillator
- Compares closing price to price range over time
- Components: %K and %D lines
- Signals:
  * Above 80: Overbought
  * Below 20: Oversold
  * %K crosses %D: Potential trend change

### C. Volatility Indicators

#### Bollinger Bands
- Upper/Lower bands: 2 standard deviations from MA
- Middle band: 20-day MA
- Signals:
  * Price touching upper band: Potential resistance
  * Price touching lower band: Potential support
  * Band squeeze: Potential breakout

#### ATR (Average True Range)
- Measures market volatility
- Higher values: More volatility
- Lower values: Less volatility
- Used for stop-loss placement and trend strength

### D. Volume Indicators

#### On-Balance Volume (OBV)
- Cumulative volume indicator
- Signals:
  * Rising OBV with rising price: Strong uptrend
  * Falling OBV with rising price: Potential reversal

#### Volume Moving Average
- Helps identify volume trends
- Above average volume: Strong price movement
- Below average volume: Weak price movement

## 3. LLM Analysis Integration

### Input data:
You are a Stock Trader specializing in Technical Analysis at a top financial institution.

I will provide you with the following technical indicators for analysis:
- Moving Averages (SMA/EMA): [20, 50, 200 periods]
- MACD: [12, 26, 9 settings]
- RSI: [14 period]
- Stochastic Oscillator: [%K and %D values]
- Bollinger Bands: [20 period, 2 standard deviations]
- ATR: [14 period]
- OBV (On-Balance Volume)
- Volume Moving Average

Based on these indicators, please provide:
1. A clear BUY/SELL/HOLD recommendation
2. Confidence level (High/Medium/Low)
3. Detailed analysis including:
   - Trend analysis (Moving Averages and MACD interpretation)
   - Momentum status (RSI and Stochastic readings)
   - Volatility assessment (Bollinger Bands and ATR)
   - Volume analysis (OBV and Volume MA)
   - Any significant indicator convergence/divergence
   - Key support/resistance levels
4. Potential entry/exit points
5. Risk considerations

Please provide your response in clear, professional language with emphasis on actionable insights.
User preferred language: English.
