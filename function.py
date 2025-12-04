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

def yearly_extreme_days(df, high_quantile = 0.99, low_quantile = 0.01):
    """
    Counts the number of yearly extreme hot and cold days based on quantiles

    Parameters:
    df:
    pandas.DataFrame
        Must contain: "Max Temp (°C)" and "Min Temp (°C)" columns
    high_quant : float
        Quantile for defining extremely hot days
    low_quant : float
        Quantile for defining extremely cold days

    Returns:
    pandas.DataFrame
        with index: year
        and columns: "extreme_hot_days", "extreme_cold_days"
    """
    df = df.copy()
    df['year'] = df.index.year
    result = []
    for year, group in df.groupby('year'):
        hot_cutoff = group["Max Temp (°C)"].quantile(high_quantile)
        cold_cutoff = group["Min Temp (°C)"].quantile(low_quantile)
    
        extreme_hot = (group["Max Temp (°C)"] > hot_cutoff).sum()
        extreme_cold = (group["Min Temp (°C)"] < cold_cutoff).sum()

        result.append({
            'year': year,
            'extreme_hot_days': extreme_hot,
            'extreme_cold_days': extreme_cold
        })
    
    return pd.DataFrame(result).set_index('year').fillna(0).astype(int)

def yearly_mean_temperature(df):
    """
    Returns yearly mean temperature.
    """
    return df.groupby(df.index.year)['Mean Temp (°C)'].mean()

def temperature_trend(years, values):
    """
    Calculates linear trend (slope, p-value) for given yearly values.
    """
    from scipy.stats import linregress
    slope, intercept, r_value, p_value, std_err = linregress(years, values)
    return slope, p_value
