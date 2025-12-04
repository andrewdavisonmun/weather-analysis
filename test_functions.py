import pandas as pd
import numpy as np
from function import daily_temperature_range, rolling_mean_temperature, yearly_extreme_days, yearly_mean_temperature, temperature_trend

def test_daily_temperature_range():
  df = pd.DataFrame({"Max Temp (°C)": [10, 20], "Min Temp (°C)": [5, 15]})
  expected = pd.Series([5,5])
  result = daily_temperature_range(df)
  assert result.equals(expected), f"Expected {expected.tolist()}, got {result.tolist()}"
