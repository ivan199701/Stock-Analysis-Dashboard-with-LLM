import logging
from typing import List, Dict, Optional, Tuple
from domain.entities.stock import Stock
from domain.value_objects.analysis_result import AnalysisResult

# Set up logging
logger = logging.getLogger(__name__)


class StockAnalysis:
    """
    Stock Analysis Aggregate Root, integrating all analysis results
    """

    # Configuration constants
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    PRICE_LEVEL_PROXIMITY = 0.02  # 2% threshold for price level proximity
    VOLUME_SURGE_THRESHOLD = 1.5
    VOLUME_LOW_THRESHOLD = 0.5
    TREND_STRENGTH_THRESHOLD = {
        'strong': 0.7,
        'moderate': 0.5,
        'weak': 0.3
    }

    def __init__(self, stock: Stock):
        self.stock = stock
        self.indicators = {}
        self.analysis_results = {}

    def analyze(self, timeframe='medium', indicators: list = None) -> AnalysisResult:
        """
        Execute complete analysis process with configurable timeframe and indicators
        Returns an AnalysisResult value object

        Args:
            timeframe: 'short' (10 periods), 'medium' (20 periods), or 'long' (50 periods)
            indicators: A list of strings specifying which indicators to calculate.

        Returns:
            AnalysisResult: Value object containing analysis results
        """
        # If no indicators are specified, use all available
        if indicators is None:
            indicators = ["SMA", "EMA", "RSI", "MACD", "Bollinger Bands", "Stochastic", "ATR", "OBV"]

        # Validate timeframe
        if timeframe not in ['short', 'medium', 'long']:
            logger.warning(f"Invalid timeframe: {timeframe}, using 'medium'")
            timeframe = 'medium'

        self._calculate_indicators(timeframe, indicators)
        self._analyze_trend(timeframe)
        self._generate_signals(timeframe)

        # Create and return an AnalysisResult value object
        return AnalysisResult(
            trend=self.analysis_results.get('trend', 'neutral'),
            strength=self.analysis_results.get('strength', 0.0),
            signals=self.analysis_results.get('signals', []),
            support_levels=self.analysis_results.get('support_levels', []),
            resistance_levels=self.analysis_results.get(
                'resistance_levels', []),
            recommendation=self.analysis_results.get('recommendation', 'HOLD'),
            indicators=self.indicators
        )

    def _calculate_indicators(self, timeframe='medium', indicators: list = None):
        """
        Calculate the selected technical indicators.
        """
        if indicators is None:
            indicators = []
            
        try:
            period = self._get_period_from_timeframe(timeframe)
            
            if "SMA" in indicators:
                self.indicators['sma'] = self.stock.calculate_sma(period=period)
            if "EMA" in indicators:
                self.indicators['ema'] = self.stock.calculate_ema(period=period)
            if "RSI" in indicators:
                self.indicators['rsi'] = self.stock.calculate_rsi(period=period)
            if "MACD" in indicators:
                self.indicators['macd'] = self.stock.calculate_macd()
            if "Bollinger Bands" in indicators:
                self.indicators['bbands'] = self.stock.calculate_bollinger_bands(period=period)
            if "Stochastic" in indicators:
                self.indicators['stoch'] = self.stock.calculate_stoch()
            if "ATR" in indicators:
                self.indicators['atr'] = self.stock.calculate_atr(period=period)
            if "OBV" in indicators:
                self.indicators['obv'] = self.stock.calculate_obv()

        except Exception as e:
            logger.error(f"Error calculating indicators: {str(e)}")
            self.indicators = {}

    def _get_period_from_timeframe(self, timeframe: str) -> int:
        """
        Convert timeframe string to period count

        Args:
            timeframe: 'short', 'medium', or 'long'

        Returns:
            int: Number of periods for calculations
        """
        if timeframe == 'short':
            return 10
        elif timeframe == 'long':
            return 50
        else:  # medium is default
            return 20

    def _analyze_trend(self, timeframe='medium'):
        """
        Analyze price trend using multiple indicators

        Args:
            timeframe: 'short', 'medium', or 'long'
        """
        # Initialize trend signals list
        trend_signals = []

        # Get indicator data
        sma = self.indicators.get('sma', [])
        rsi = self.indicators.get('rsi', [])
        macd = self.indicators.get('macd', {})

        # Get recent prices
        if not self.stock.prices:
            logger.warning("No price data available for trend analysis")
            self.analysis_results['trend'] = 'neutral'
            self.analysis_results['strength'] = 0.0
            return

        current_price = self.stock.prices[-1].close

        # 1. SMA Analysis
        if sma and len(sma) > 0:
            current_sma = sma[-1]
            if current_price > current_sma:
                trend_signals.append(('bullish', 0.6))
            else:
                trend_signals.append(('bearish', 0.6))

            # Price momentum relative to SMA
            # Adjust lookback based on timeframe
            sma_lookback = self._get_lookback_period(timeframe)
            sma_lookback = min(sma_lookback, len(sma))

            if sma_lookback > 0:
                try:
                    # Safe division with zero check
                    sma_value = sma[-sma_lookback]
                    price_momentum = (current_price - sma_value) / \
                        sma_value if sma_value > 0 else 0

                    # Adjust thresholds based on timeframe
                    momentum_threshold = 0.01 if timeframe == 'short' else 0.02 if timeframe == 'medium' else 0.03

                    if price_momentum > momentum_threshold:
                        trend_signals.append(('bullish', 0.7))
                    elif price_momentum < -momentum_threshold:
                        trend_signals.append(('bearish', 0.7))
                except (IndexError, ZeroDivisionError) as e:
                    logger.warning(
                        f"Error calculating price momentum: {str(e)}")

        # 2. RSI Analysis
        if rsi and len(rsi) > 0:
            current_rsi = rsi[-1]
            if current_rsi > self.RSI_OVERBOUGHT:
                trend_signals.append(('bearish', 0.8))  # Overbought
            elif current_rsi < self.RSI_OVERSOLD:
                trend_signals.append(('bullish', 0.8))  # Oversold
            elif current_rsi > 50 and current_rsi < self.RSI_OVERBOUGHT:
                trend_signals.append(('bullish', 0.3))  # Bullish momentum
            elif current_rsi < 50 and current_rsi > self.RSI_OVERSOLD:
                trend_signals.append(('bearish', 0.3))  # Bearish momentum

        # 3. MACD Analysis
        if macd and 'macd' in macd and 'signal' in macd and len(macd['macd']) > 1 and len(macd['signal']) > 1:
            current_macd = macd['macd'][-1]
            prev_macd = macd['macd'][-2]
            current_signal = macd['signal'][-1]
            prev_signal = macd['signal'][-2]

            # MACD Crossover
            if prev_macd < prev_signal and current_macd > current_signal:
                trend_signals.append(('bullish', 0.7))  # Bullish crossover
            elif prev_macd > prev_signal and current_macd < current_signal:
                trend_signals.append(('bearish', 0.7))  # Bearish crossover

            # MACD above/below zero
            if current_macd > 0:
                trend_signals.append(('bullish', 0.5))
            else:
                trend_signals.append(('bearish', 0.5))

        # Determine overall trend based on signals
        if not trend_signals:
            self.analysis_results['trend'] = 'neutral'
            self.analysis_results['strength'] = 0.0
            return

        # Calculate trend and strength
        self._calculate_trend_and_strength(trend_signals, timeframe)

    def _calculate_trend_and_strength(self, trend_signals: List[Tuple[str, float]], timeframe: str):
        """
        Calculate overall trend and strength from individual signals

        Args:
            trend_signals: List of (trend, strength) tuples
            timeframe: Analysis timeframe
        """
        # Count trend signals
        bullish_count = sum(
            1 for signal in trend_signals if signal[0] == 'bullish')
        bearish_count = sum(
            1 for signal in trend_signals if signal[0] == 'bearish')

        # Calculate strength as weighted average
        total_weight = sum(signal[1] for signal in trend_signals)
        bullish_weight = sum(
            signal[1] for signal in trend_signals if signal[0] == 'bullish')
        bearish_weight = sum(
            signal[1] for signal in trend_signals if signal[0] == 'bearish')

        if bullish_count > bearish_count:
            self.analysis_results['trend'] = 'bullish'
            self.analysis_results['strength'] = bullish_weight / \
                total_weight if total_weight > 0 else 0.0
        elif bearish_count > bullish_count:
            self.analysis_results['trend'] = 'bearish'
            self.analysis_results['strength'] = bearish_weight / \
                total_weight if total_weight > 0 else 0.0
        else:
            # Equal signals, determine by weight
            if bullish_weight > bearish_weight:
                self.analysis_results['trend'] = 'bullish'
                self.analysis_results['strength'] = bullish_weight / \
                    total_weight if total_weight > 0 else 0.0
            elif bearish_weight > bullish_weight:
                self.analysis_results['trend'] = 'bearish'
                self.analysis_results['strength'] = bearish_weight / \
                    total_weight if total_weight > 0 else 0.0
            else:
                self.analysis_results['trend'] = 'neutral'
                self.analysis_results['strength'] = 0.5

        # Add trend confirmation mechanism
        # Adjust confirmation period based on timeframe
        confirmation_period = 2 if timeframe == 'short' else 3 if timeframe == 'medium' else 5
        if not self._confirm_trend(trend_signals, confirmation_period):
            # If trend is not confirmed, reduce strength
            self.analysis_results['strength'] *= 0.7

    def _get_lookback_period(self, timeframe: str) -> int:
        """
        Get appropriate lookback period based on timeframe

        Args:
            timeframe: Analysis timeframe

        Returns:
            int: Lookback period
        """
        if timeframe == 'short':
            return 3
        elif timeframe == 'long':
            return 10
        else:  # medium
            return 5

    def _confirm_trend(self, trend_signals, confirmation_period=3):
        """
        Confirm trend by checking if recent signals are consistent

        Args:
            trend_signals: List of (trend, strength) tuples
            confirmation_period: Number of consecutive signals to check

        Returns:
            bool: True if trend is confirmed, False otherwise
        """
        if len(trend_signals) < confirmation_period:
            return True  # Insufficient data, cannot confirm, default to confirmed

        # Get recent trend signals
        recent_signals = trend_signals[-confirmation_period:]
        trends = [signal[0] for signal in recent_signals]

        # Check if all trend signals are consistent
        return all(trend == trends[0] for trend in trends)

    def _generate_signals(self, timeframe='medium'):
        """
        Generate trading signals based on technical indicators

        Args:
            timeframe: 'short', 'medium', or 'long'
        """
        signals = []

        # Get indicator data
        rsi = self.indicators.get('rsi', [])
        macd = self.indicators.get('macd', {})
        bbands = self.indicators.get('bbands', {})

        if not self.stock.prices:
            self.analysis_results['signals'] = []
            return

        # Get current price data
        current_price = self.stock.prices[-1].close

        # 1. RSI Signals
        if rsi and len(rsi) > 0:
            current_rsi = rsi[-1]
            if current_rsi > self.RSI_OVERBOUGHT:
                signals.append("RSI Overbought")
            elif current_rsi < self.RSI_OVERSOLD:
                signals.append("RSI Oversold")

        # 2. MACD Signals
        if macd and 'macd' in macd and 'signal' in macd and len(macd['macd']) > 1 and len(macd['signal']) > 1:
            current_macd = macd['macd'][-1]
            prev_macd = macd['macd'][-2]
            current_signal = macd['signal'][-1]
            prev_signal = macd['signal'][-2]

            if prev_macd < prev_signal and current_macd > current_signal:
                signals.append("MACD Bullish Crossover")
            elif prev_macd > prev_signal and current_macd < current_signal:
                signals.append("MACD Bearish Crossover")

        # 3. Bollinger Bands Signals
        if bbands and 'upper' in bbands and 'lower' in bbands and len(bbands['upper']) > 0 and len(bbands['lower']) > 0:
            upper_band = bbands['upper'][-1]
            lower_band = bbands['lower'][-1]

            if current_price > upper_band:
                signals.append("Price Above Upper Bollinger Band")
            elif current_price < lower_band:
                signals.append("Price Below Lower Bollinger Band")

        # 4. Volume Analysis
        period = self._get_period_from_timeframe(timeframe)
        volume_factor = self._analyze_volume(period)
        if volume_factor > self.VOLUME_SURGE_THRESHOLD:
            signals.append("Volume Surge")
        elif volume_factor < self.VOLUME_LOW_THRESHOLD:
            signals.append("Low Volume")

        # 5. Support/Resistance Analysis
        if len(self.stock.prices) > 10:
            prices = [price.close for price in self.stock.prices]

            # Identify support and resistance levels
            support_levels = self._identify_support_levels(prices, timeframe)
            resistance_levels = self._identify_resistance_levels(
                prices, timeframe)

            # Store levels in analysis results
            self.analysis_results['support_levels'] = support_levels
            self.analysis_results['resistance_levels'] = resistance_levels

            # Check if price is near support or resistance
            for support in support_levels:
                # Safe division with zero check
                if support > 0 and abs(current_price - support) / support < self.PRICE_LEVEL_PROXIMITY:
                    signals.append(f"Near Support Level: {support:.2f}")
                    break

            for resistance in resistance_levels:
                # Safe division with zero check
                if resistance > 0 and abs(current_price - resistance) / resistance < self.PRICE_LEVEL_PROXIMITY:
                    signals.append(f"Near Resistance Level: {resistance:.2f}")
                    break

        # Store signals in analysis results
        self.analysis_results['signals'] = signals

        # Generate recommendation
        trend = self.analysis_results.get('trend', 'neutral')
        strength = self.analysis_results.get('strength', 0.0)

        recommendation = self._generate_recommendation(
            trend, strength, signals, timeframe)
        self.analysis_results['recommendation'] = recommendation

    def _analyze_volume(self, period=20):
        """
        Analyze volume to confirm price movements

        Args:
            period: Number of periods to analyze

        Returns:
            float: Volume factor (current volume / average volume)
        """
        try:
            # Try to get volume data
            volume_period = min(period, len(self.stock.prices))
            if volume_period <= 0:
                return 1.0  # Default value

            recent_volumes = [
                price.volume for price in self.stock.prices[-volume_period:]]
            if not recent_volumes:
                return 1.0  # Default value

            avg_volume = sum(recent_volumes) / len(recent_volumes)
            current_volume = recent_volumes[-1]

            # Calculate volume factor (ratio of current volume to average volume)
            volume_factor = current_volume / avg_volume if avg_volume > 0 else 1.0
            return volume_factor
        except (AttributeError, ZeroDivisionError, IndexError) as e:
            logger.warning(f"Error analyzing volume: {str(e)}")
            # If data is unavailable or error occurs, return default value
            return 1.0

    def _identify_support_levels(self, prices: List[float], timeframe='medium') -> List[float]:
        """
        Identify key support levels based on historical lows
        Uses a weighted algorithm to find significant price levels

        Args:
            prices: List of closing prices
            timeframe: Analysis timeframe ('short', 'medium', 'long')

        Returns:
            List[float]: Support levels sorted from highest to lowest
        """
        if len(prices) < 10:
            return []

        # Adjust window size based on timeframe
        if timeframe == 'short':
            window_size = max(3, len(prices) // 30)
        elif timeframe == 'medium':
            window_size = max(3, len(prices) // 20)
        else:  # long
            window_size = max(3, len(prices) // 10)

        support_levels = []
        support_strengths = {}  # Track how significant each level is

        # Find local minima (with adaptive window)
        for i in range(window_size, len(prices) - window_size):
            # Check if this point is a local minimum
            if all(prices[i] <= prices[i-j] for j in range(1, window_size)) and \
               all(prices[i] <= prices[i+j] for j in range(1, window_size)):
                support_level = prices[i]

                # Find or create a "price zone" rather than exact price
                matched = False
                for existing in list(support_strengths.keys()):
                    # Safe division with zero check
                    if existing > 0 and abs(support_level - existing) / existing < self.PRICE_LEVEL_PROXIMITY:
                        support_strengths[existing] += 1
                        matched = True
                        break

                if not matched:
                    support_strengths[support_level] = 1

        # Convert to list of (level, strength) tuples and sort by strength
        support_items = list(support_strengths.items())
        support_items.sort(key=lambda x: x[1], reverse=True)

        # Get levels only, sorted by price (highest first)
        current_price = prices[-1]
        supports_below = sorted(
            [level for level, _ in support_items if level < current_price],
            reverse=True
        )

        return supports_below[:3]  # Return top 3 support levels

    def _identify_resistance_levels(self, prices: List[float], timeframe='medium') -> List[float]:
        """
        Identify key resistance levels based on historical highs
        Uses a weighted algorithm to find significant price levels

        Args:
            prices: List of closing prices
            timeframe: Analysis timeframe ('short', 'medium', 'long')

        Returns:
            List[float]: Resistance levels sorted from lowest to highest
        """
        if len(prices) < 10:
            return []

        # Adjust window size based on timeframe
        if timeframe == 'short':
            window_size = max(3, len(prices) // 30)
        elif timeframe == 'medium':
            window_size = max(3, len(prices) // 20)
        else:  # long
            window_size = max(3, len(prices) // 10)

        resistance_levels = []
        resistance_strengths = {}  # Track how significant each level is

        # Find local maxima (with adaptive window)
        for i in range(window_size, len(prices) - window_size):
            # Check if this point is a local maximum
            if all(prices[i] >= prices[i-j] for j in range(1, window_size)) and \
               all(prices[i] >= prices[i+j] for j in range(1, window_size)):
                resistance_level = prices[i]

                # Find or create a "price zone" rather than exact price
                matched = False
                for existing in list(resistance_strengths.keys()):
                    # Safe division with zero check
                    if existing > 0 and abs(resistance_level - existing) / existing < self.PRICE_LEVEL_PROXIMITY:
                        resistance_strengths[existing] += 1
                        matched = True
                        break

                if not matched:
                    resistance_strengths[resistance_level] = 1

        # Convert to list of (level, strength) tuples and sort by strength
        resistance_items = list(resistance_strengths.items())
        resistance_items.sort(key=lambda x: x[1], reverse=True)

        # Get levels only, sorted by price (lowest first)
        current_price = prices[-1]
        resistances_above = sorted(
            [level for level, _ in resistance_items if level > current_price]
        )

        return resistances_above[:3]  # Return top 3 resistance levels

    def _generate_recommendation(self, trend: str, strength: float, signals: List[str], timeframe='medium') -> str:
        """
        Generate trading recommendation based on analysis

        Args:
            trend: 'bullish', 'bearish', or 'neutral'
            strength: Trend strength (0.0 to 1.0)
            signals: List of generated signals
            timeframe: Analysis timeframe ('short', 'medium', 'long')

        Returns:
            str: Trading recommendation ('BUY', 'SELL', or 'HOLD')
        """
        # Adjust strength thresholds based on timeframe
        strength_threshold = 0.6 if timeframe == 'short' else 0.7 if timeframe == 'medium' else 0.8

        # Volume confirmation signal
        volume_confirmation = any(
            "Volume Surge" in signal for signal in signals)

        # Strong signals with volume confirmation
        if "RSI Oversold" in signals and trend == "bullish" and strength > strength_threshold and volume_confirmation:
            return "BUY"
        elif "RSI Overbought" in signals and trend == "bearish" and strength > strength_threshold and volume_confirmation:
            return "SELL"
        elif "MACD Bullish Crossover" in signals and trend == "bullish" and strength > strength_threshold:
            return "BUY"
        elif "MACD Bearish Crossover" in signals and trend == "bearish" and strength > strength_threshold:
            return "SELL"

        # Strong signals without volume confirmation
        elif "RSI Oversold" in signals and trend == "bullish" and strength > strength_threshold + 0.1:
            return "BUY"
        elif "RSI Overbought" in signals and trend == "bearish" and strength > strength_threshold + 0.1:
            return "SELL"

        # Moderate signals
        elif trend == "bullish" and strength > 0.8:
            return "BUY"
        elif trend == "bearish" and strength > 0.8:
            return "SELL"

        # Support/resistance breakouts
        elif any("Support Level" in signal for signal in signals) and trend == "bullish" and strength > 0.6:
            return "BUY"
        elif any("Resistance Level" in signal for signal in signals) and trend == "bearish" and strength > 0.6:
            return "SELL"

        # Default recommendation
        return "HOLD"

    def get_analysis_results(self) -> Dict:
        """
        Get analysis results

        Returns:
            Dict: Dictionary containing all analysis results
        """
        return self.analysis_results
