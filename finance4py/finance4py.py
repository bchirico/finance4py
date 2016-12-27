# -*- coding: utf-8 -*-

import numpy as np
from pandas import DataFrame


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
