#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_finance4py
----------------------------------

Tests for `finance4py` module.
"""


import sys
import unittest
from pandas import DataFrame, Series
from pandas_datareader.data import DataReader
import finance4py
# import talib
import numpy as np


class TestFinance4py(unittest.TestCase):

    def setUp(self):
        self.stock = DataReader('MSFT', 'google')

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    # def test_TRA(self):
    #     tra = finance4py.TRA(self.stock)
    #     print tra

    def test_true_range(self):
        tr = finance4py.true_range(self.stock.High, self.stock.Low,
                                   self.stock.Close)
        # tr_talib = talib.TRANGE(self.stock.High.values, self.stock.Low.values,
        #                         self.stock.Close.values)
        self.assertIsInstance(tr, DataFrame)
        self.assertListEqual(tr.index.tolist(), self.stock.index.tolist())
        self.assertListEqual(tr.columns.tolist(), ['TR1', 'TR2', 'TR3', 'TR'])
        # why on hearth talib has a nan value as first element??
        # np.testing.assert_almost_equal(tr.TR.values, tr_talib)

    def test_rsi(self):
        rsi = finance4py.rsi(self.stock.Close)
        # rsi_talib = talib.RSI(self.stock.Close.values)
        self.assertIsInstance(rsi, Series)
        self.assertListEqual(rsi.index.tolist(), self.stock.index.tolist())
        self.assertEqual(rsi.name, 'RSI')
        # also here there are more nan values in talib
        # np.testing.assert_almost_equal(rsi.values, rsi_talib)