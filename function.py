import pandas as pd

def daily_temperature_range(df):
    """
    Calculates daily temperature range for a weather DataFrame.

    Parameters
    df : pandas DataFrame
        with Columns:
        - "Max Temp (°C)"
        - "Min Temp (°C)"

    Returns
    pandas Series
    with index:
    date
    and values:
    Max Temp (°C) - Min Temp (°C)
    """
    if "Max Temp (°C)" not in df.columns or "Min Temp (°C)" not in df.columns:
        raise ValueError("DataFrame must contain max and min temperature columns.")

    max_t = pd.to_numeric(df["Max Temp (°C)"], errors="coerce")
    min_t = pd.to_numeric(df["Min Temp (°C)"], errors="coerce")

    return max_t - min_t

def rolling_mean_temperature(df, window=30):
    """
    Calculates a rolling average of the mean temperature.

    Parameters:
    df : 
    pandas.DataFrame
        Must contain: "Mean Temp (°C)"

    window : 
    int
        Rolling window size in days

    Returns:
    pandas.Series
        N day rolling mean temperature. 30 by default
    """
    temps = pd.to_numeric(df["Mean Temp (°C)"], errors="coerce")
    return temps.rolling(window=window, min_periods=1).mean()
