import pandas as pd
import numpy as np
from function import daily_temperature_range, rolling_mean_temperature, yearly_extreme_days, yearly_mean_temperature, temperature_trend

def test_daily_temperature_range():
  df = pd.DataFrame({"Max Temp (°C)": [10, 20], "Min Temp (°C)": [5, 15]})
  expected = pd.Series([5,5])
  result = daily_temperature_range(df)
  assert result.equals(expected), f"Expected {expected.tolist()}, got {result.tolist()}"

def test_daily_temperature_range_with_nan():
  df = pd.DataFrame({"Max Temp (°C)": [10, np.nan], "Min Temp (°C)": [5, 2]})
  expected = pd.Series([5,np.nan])
  result = daily_temperature_range(df)
  assert result.equals(expected), f"Expected {expected.tolist()}, got {result.tolist()}"

def test_rolling_mean_temperature():
  df = pd.DataFrame({"Mean Temp (°C)": [10, 20, 30, 40]})
  expected = pd.Series([10.0, 15.0, 25.0, 35.0])
  result = rolling_mean_temperature(df, window = 2)
  assert result.equals(expected), f"Expected {expected.tolist()}, got {result.tolist()}"

def test_rolling_mean_temperature_window1():
  df = pd.DataFrame({"Mean Temp (°C)": [5, 15, 25]})
  expected = pd.Series([5.0, 15.0, 25.0])
  result = rolling_mean_temperature(df, window = 1)
  assert result.equals(expected), f"Expected {expected.tolist()}, got {result.tolist()}"

def test_yearly_extreme_days():
  dates = pd.date_range(start="2011-01-01", periods = 4)
  df = pd.DataFrame({"Max Temp (°C)": [10, 50, 20, 5], "Min Temp (°C)": [0, 30, -10, -20]}, index = dates)
  result = yearly_extreme_days(df, high_quantile = 0.75, low_quantile = 0.25)
  expected = pd.DataFrame({"extreme_hot_days": [1], "extreme_cold_days": [1]}, index=pd.Index([2011], dtype=result.index.dtype, name='year'))
  pd.testing.assert_frame_equal(result, expected)
