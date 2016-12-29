# -*- coding: utf-8 -*-

import numpy as np
from pandas import DataFrame
import pandas as pd
from matplotlib.pyplot import show


def bbands(close_price, window=30, numsd=2):
    """ returns average, upper band, and lower band"""
    average = close_price.rolling(window=window, center=False).mean()
    std = close_price.rolling(window=window, center=False).std()
    upband = average + (std*numsd)
    dnband = average - (std*numsd)
    boll_bands = DataFrame.from_dict({
        'close': close_price,
        'close_average': np.round(average, 3),
        'bb_upper': np.round(upband, 3),
        'bb_lower': np.round(dnband, 3)
    })
    return boll_bands


def true_range(stock):
    """
    True Range (TR), which is defined as the greatest of the following:

    - Current High less the current Low
    - Current High less the previous Close (absolute value)
    - Current Low less the previous Close (absolute value)

    :param stock: Pandas DataFrame
    :return: TR: the true range calculated as above
    """
    tr = DataFrame()
    tr['TR1'] = abs(stock['High'] - stock['Low'])
    tr['TR2'] = abs(stock['High'] - stock['Close'].shift())
    tr['TR3'] = abs(stock['Low'] - stock['Close'].shift())
    tr['TR'] = tr[['TR1', 'TR2', 'TR3']].max(axis=1)

    return tr


def average_true_range(stock, window=14):
    """
    Average True range. It's an indicator that measure volatility.

    https://stockcharts.com/school/doku.php?id=chart_school:\
    technical_indicators:average_true_range_atr

    https://en.wikipedia.org/wiki/Average_true_range

    :param stock: pandas DataFrame
    :param window: int.
    :return:
    """
    tr = true_range(stock)
    atr = [np.nan] * tr.shape[0]
    atr[window] = tr['TR'].iloc[:window].mean()
    for i in range(window+1, len(atr)):
        atr[i] = (atr[i-1] * (window - 1) + tr['TR'].iloc[i]) / window
    tr['ATR'] = atr
    return tr


def rsi(stock, window=14):
    delta = stock['Close'].diff()[1:]

    up, down = delta.copy(), delta.copy()

    # can't remember why did this
    up[up < 0] = 0
    down[down > 0] = 0

    roll_up = pd.stats.moments.ewma(up, window)
    roll_down = pd.stats.moments.ewma(down.abs(), window)

    rs = roll_up / roll_down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    rsi.columns = ['rsi']
    return rsi[1:]
