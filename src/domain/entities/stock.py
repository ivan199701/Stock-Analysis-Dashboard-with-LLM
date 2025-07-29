from dataclasses import dataclass
from typing import List, Dict
from domain.value_objects.price import Price
import pandas as pd
import pandas_ta as ta


@dataclass
class Stock:
    symbol: str
    name: str
    prices: List[Price]

    def _get_dataframe(self) -> pd.DataFrame:
        data = {
            'timestamp': [price.timestamp for price in self.prices],
            'open': [price.open for price in self.prices],
            'high': [price.high for price in self.prices],
            'low': [price.low for price in self.prices],
            'close': [price.close for price in self.prices],
            'volume': [price.volume for price in self.prices]
        }
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        return df

    def calculate_sma(self, period: int = 20) -> List[float]:
        df = self._get_dataframe()
        return df.ta.sma(length=period).tolist()

    def calculate_ema(self, period: int = 20) -> List[float]:
        df = self._get_dataframe()
        return df.ta.ema(length=period).tolist()

    def calculate_rsi(self, period: int = 14) -> List[float]:
        df = self._get_dataframe()
        return df.ta.rsi(length=period).tolist()

    def calculate_macd(self) -> Dict[str, List[float]]:
        df = self._get_dataframe()
        macd = df.ta.macd()
        return {
            'macd': macd[f'MACD_{macd.columns[0].split("_")[1]}_{macd.columns[0].split("_")[2]}_{macd.columns[2].split("_")[2]}'].tolist(),
            'signal': macd[f'MACDs_{macd.columns[0].split("_")[1]}_{macd.columns[0].split("_")[2]}_{macd.columns[2].split("_")[2]}'].tolist(),
            'histogram': macd[f'MACDh_{macd.columns[0].split("_")[1]}_{macd.columns[0].split("_")[2]}_{macd.columns[2].split("_")[2]}'].tolist()
        }

    def calculate_bollinger_bands(self, period: int = 20, std_dev: float = 2.0) -> Dict[str, List[float]]:
        df = self._get_dataframe()
        bbands = df.ta.bbands(length=period, std=std_dev)
        return {
            'upper': bbands[f'BBU_{period}_{std_dev}'].tolist(),
            'middle': bbands[f'BBM_{period}_{std_dev}'].tolist(),
            'lower': bbands[f'BBL_{period}_{std_dev}'].tolist()
        }

    def calculate_stoch(self) -> Dict[str, List[float]]:
        df = self._get_dataframe()
        stoch = df.ta.stoch()
        return {
            'k': stoch[stoch.columns[0]].tolist(),
            'd': stoch[stoch.columns[1]].tolist()
        }

    def calculate_atr(self, period: int = 14) -> List[float]:
        df = self._get_dataframe()
        return df.ta.atr(length=period).tolist()

    def calculate_obv(self) -> List[float]:
        df = self._get_dataframe()
        return df.ta.obv().tolist()