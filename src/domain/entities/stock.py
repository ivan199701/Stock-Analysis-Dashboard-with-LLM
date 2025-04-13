from dataclasses import dataclass
from typing import List, Dict
from ..value_objects.price import Price
import pandas as pd
import pandas_ta as ta


@dataclass
class Stock:
    """
    Stock Entity Class
    """
    symbol: str
    name: str
    prices: List[Price]

    def _get_dataframe(self) -> pd.DataFrame:
        """Convert price list to pandas DataFrame"""
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
        sma = df.ta.sma(length=period)
        return sma.tolist()

    def calculate_rsi(self, period: int = 14) -> List[float]:
        df = self._get_dataframe()
        rsi = df.ta.rsi(length=period)
        return rsi.tolist()

    def calculate_macd(self) -> Dict[str, List[float]]:
        df = self._get_dataframe()
        macd = df.ta.macd()

        return {
            'macd': macd['MACD_12_26_9'].tolist(),
            'signal': macd['MACDs_12_26_9'].tolist(),
            'histogram': macd['MACDh_12_26_9'].tolist()
        }

    def calculate_bollinger_bands(self, period: int = 20, std_dev: float = 2.0) -> Dict[str, List[float]]:
        df = self._get_dataframe()
        bbands = df.ta.bbands(length=period, std=std_dev)

        return {
            'upper': bbands['BBU_20_2.0'].tolist(),
            'middle': bbands['BBM_20_2.0'].tolist(),
            'lower': bbands['BBL_20_2.0'].tolist()
        }

    # def calculate_ichimoku(self) -> Dict[str, List[float]]:
    #     df = self._get_dataframe()
    #     ichimoku = df.ta.ichimoku()

    #     return {
    #         'tenkan_sen': ichimoku['ISA_9'].tolist(),
    #         'kijun_sen': ichimoku['ISB_26'].tolist(),
    #         'senkou_span_a': ichimoku['ITS_9'].tolist(),
    #         'senkou_span_b': ichimoku['IKS_26'].tolist(),
    #         'chikou_span': ichimoku['ICS_26'].tolist()
    #     }
