import random
from decimal import Decimal

from hummingbot.data_feed.candles_feed.candles_factory import CandlesConfig, CandlesFactory
from hummingbot.strategy.directional_strategy_base import DirectionalStrategyBase


class PDR(DirectionalStrategyBase):
    """
    A template strategy implementation based on the DirectionalStrategyBase.

    This strategy uses a random number generator to create trading signals and execute trades based on the random number values.
    It defines the specific parameters and configurations for the strategy.

    Parameters:
        directional_strategy_name (str): The name of the strategy.
        trading_pair (str): The trading pair to be traded.
        exchange (str): The exchange to be used for trading.
        order_amount_usd (Decimal): The amount of the order in USD.
        leverage (int): The leverage to be used for trading.

    Position Parameters:
        stop_loss (float): The stop-loss percentage for the position.
        take_profit (float): The take-profit percentage for the position.
        time_limit (int): The time limit for the position in seconds.
        trailing_stop_activation_delta (float): The activation delta for the trailing stop.
        trailing_stop_trailing_delta (float): The trailing delta for the trailing stop.

    Candlestick Configuration:
        candles (List[CandlesBase]): The list of candlesticks used for generating signals.

    Markets:
        A dictionary specifying the markets and trading pairs for the strategy.

    Methods:
        get_signal(): Generates the trading signal based on the RSI indicator.
        get_processed_df(): Retrieves the processed dataframe with RSI values.
        market_data_extra_info(): Provides additional information about the market data.

    Inherits from:
        DirectionalStrategyBase: Base class for creating directional strategies using the PositionExecutor.
    """
    directional_strategy_name: str = "PDR"
    # Define the trading pair and exchange that we want to use and the csv where we are going to store the entries
    trading_pair: str = "BTC-USD"
    exchange: str = "dydx_perpetual"
    order_amount_usd = Decimal("38")
    leverage = 1

    # Configure the parameters for the position
    stop_loss: float = 0.0075
    take_profit: float = 0.015
    time_limit: int = 60 * 1
    trailing_stop_activation_delta = 0.004
    trailing_stop_trailing_delta = 0.001
    cooldown_after_execution = 10

    candles = [CandlesFactory.get_candle(CandlesConfig(connector="binance", trading_pair="BTC-USDT", interval="5m", max_records=1000))]
    markets = {exchange: {trading_pair}}

    def get_signal(self):
        """
        Generates the trading signal based on the random numbers.
        Returns:
            int: The trading signal (-1 for sell, 0 for hold, 1 for buy).
        """

        if random.randint(1, 100) > 50:
            return -1
        elif random.randint(1, 100) < 49:
            return 1
        else:
            return 0

    def get_processed_df(self):
        """
        Retrieves the processed dataframe.
        Returns:
            pd.DataFrame: The processed dataframe.
        """
        candles_df = self.candles[0].candles_df
        return candles_df

    def market_data_extra_info(self):
        """
        Provides additional information about the market data to the format status.
        Returns:
            List[str]: A list of formatted strings containing market data information.
        """
        lines = []
        columns_to_show = ["timestamp", "open", "low", "high", "close", "volume"]
        candles_df = self.get_processed_df()
        lines.extend([f"Candles: {self.candles[0].name} | Interval: {self.candles[0].interval}\n"])
        lines.extend(self.candles_formatted_list(candles_df, columns_to_show))
        return lines
