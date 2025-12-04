import pandas as pd
import numpy as np
from function import daily_temperature_range, rolling_mean_temperature, yearly_extreme_days, yearly_mean_temperature, temperature_trend

# daily_temperature_range
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

def test_daily_temperature_range_negative():
  df = pd.DataFrame({"Max Temp (°C)": [0, -5], "Min Temp (°C)": [-10, -15]})
  expected = pd.Series([10,10])
  result = daily_temperature_range(df)
  assert result.equals(expected), f"Expected {expected.tolist()}, got {result.tolist()}"


# rolling_mean_temperature
def test_rolling_mean_temperature():
  df = pd.DataFrame({"Mean Temp (°C)": [10, 20, 30, 40]})
  expected = pd.Series([10.0, 15.0, 25.0, 35.0])
  result = rolling_mean_temperature(df, window = 2)
  np.testing.assert_allclose(result.values, expected.values)

def test_rolling_mean_temperature_window1():
  df = pd.DataFrame({"Mean Temp (°C)": [5, 15, 25]})
  expected = pd.Series([5.0, 15.0, 25.0])
  result = rolling_mean_temperature(df, window = 1)
  np.testing.assert_allclose(result.values, expected.values)

def test_rolling_mean_temperature_with_nan():
  df = pd.DataFrame({"Mean Temp (°C)": [10, np.nan, 20]})
  expected = pd.Series([10.0, 10.0, 20.0])
  result = rolling_mean_temperature(df, window = 2)
  np.testing.assert_allclose(result.values, expected.values, equal_nan = True)

# yearly_extreme_days
def test_yearly_extreme_days():
  dates = pd.date_range(start="2011-01-01", periods = 4)
  df = pd.DataFrame({"Max Temp (°C)": [10, 50, 20, 5], "Min Temp (°C)": [0, 30, -10, -20]}, index = dates)
  result = yearly_extreme_days(df, high_quantile = 0.75, low_quantile = 0.25)
  expected = pd.DataFrame({"extreme_hot_days": [1], "extreme_cold_days": [1]}, index=pd.Index([2011], dtype=result.index.dtype, name='year'))
  pd.testing.assert_frame_equal(result, expected)

def test_yearly_extreme_days_multiple_years():
  dates = pd.date_range(start="2011-12-31", periods = 5)
  df = pd.DataFrame({"Max Temp (°C)": [10, 50, 20, 5, 15], "Min Temp (°C)": [0, 30, -10, -20, 5]}, index = dates)
  result = yearly_extreme_days(df, high_quantile = 0.6, low_quantile = 0.4)
  expected = pd.DataFrame({"extreme_hot_days": [0, 2], "extreme_cold_days": [0, 2]}, index=pd.Index([2011, 2012], dtype=result.index.dtype, name='year'))
  pd.testing.assert_frame_equal(result, expected)

def test_yearly_extreme_days_no_extremes():
  dates = pd.date_range(start="2011-01-01", periods = 3)
  df = pd.DataFrame({"Max Temp (°C)": [10, 10, 10], "Min Temp (°C)": [5, 5, 5]}, index = dates)
  result = yearly_extreme_days(df, high_quantile = 0.9, low_quantile = 0.1)
  expected = pd.DataFrame({"extreme_hot_days": [0], "extreme_cold_days": [0]}, index=pd.Index([2011], dtype=result.index.dtype, name='year'))
  pd.testing.assert_frame_equal(result, expected)

# yearly_mean_temperature
def test_yearly_mean_temperature():
  dates = pd.date_range(start="2011-01-01", periods = 4)
  df = pd.DataFrame({"Mean Temp (°C)": [10, 20, 30, 40]}, index = dates)
  result = yearly_mean_temperature(df)
  expected = pd.Series([25.0], index=pd.Index([2011], dtype=result.index.dtype, name='year'))
  np.testing.assert_allclose(results.values, expected.values)

def test_yearly_mean_temperature_multiple_years():
  dates = pd.date_range(start="2011-12-31", periods = 5)
  df = pd.DataFrame({"Mean Temp (°C)": [10, 20, 30, 40, 50]}, index = dates)
  result = yearly_mean_temperature(df)
  expected = pd.Series([20.0, 45.0], index=pd.Index([2011, 2012], dtype=result.index.dtype, name='year'))
  np.testing.assert_allclose(results.values, expected.values)
  
# temperature_trend
def test_temperature_trend():
  years = [2020, 2021, 2022]
  values = [10, 20, 30]
  slope, p_value = temperature_trend(years, values)
  assert round(slope, 5) == 10.0, f"Expected slope 10.0, got {slope}"
  assert 0 <= p_value <= 1, f"p-value out of bounds: {p_value}"
