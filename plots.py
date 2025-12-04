#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 13:44:25 2025

@author: andrewdavison
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv("toronto_citycentre_daily_2005_2025.csv")

df["Date/Time"] = pd.to_datetime(df["Date/Time"], errors="coerce")

df = df.dropna(subset=["Date/Time"])

df = df[(df["Date/Time"] >= "2005-01-01") & (df["Date/Time"] <= "2025-12-31")]

df = df.sort_values("Date/Time")

df = df[df["Date/Time"] >= "2011-01-01"]

df = df.set_index("Date/Time")

for col in ["Max Temp (°C)", "Min Temp (°C)", "Mean Temp (°C)"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    
def plot_temperature(df):
    plt.figure(figsize=(12,5))
    plt.plot(df.index, df["Max Temp (°C)"], color="red", alpha=0.6, label="Max Temp")
    plt.plot(df.index, df["Min Temp (°C)"], color="blue", alpha=0.6, label="Min Temp")

    plt.title("Toronto City Centre — Daily Temperatures (2011–2025)")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    plt.xticks(rotation=45)
    plt.xlim([df.index.min(), df.index.max()])
    plt.tight_layout()
    plt.show()
plot_temperature(df)

df["Temp_Range"] = daily_temperature_range(df)

plt.figure(figsize=(12,5))
plt.plot(df.index, df["Temp_Range"], color = 'purple')
plt.title("Daily Temperature Range (Max - Min)")
plt.xlabel("Date")
plt.ylabel("Temperature Range (°C)")
plt.show()

df["Rolling_Mean"] = rolling_mean_temperature(df, window = 30)
plt.figure(figsize=(12,5))
plt.plot(df.index, df["Mean Temp (°C)"], alpha = 0.4, label = 'Daily Mean')
plt.plot(df.index, df["Rolling_Mean"], color = "orange", label = '30-Day Rolling Mean')
plt.title("Toronto Mean Temperature with 30-Day Rolling Average")
plt.xlabel("Date")
plt.ylabel("Temperature Range (°C)")
plt.legend()
plt.show()

yearly_extremes = yearly_extreme_days(df)
yearly_extremes.plot(kind = "bar", figsize = (12,5))
plt.title("Yearly Extreme Hot and Cold Days")
plt.xlabel("Year")
plt.ylabel("Number of Extreme Days")
plt.xticks(rotation = 45)
plt.legend()
plt.show()

yearly_mean = yearly_mean_temperature(df)
slope, p_value = temperature_trend(yearly_mean.index, yearly_mean.values)

plt.figure(figsize=(12,5))
plt.plot(yearly_mean.index, yearly_mean.values, marker = 'o', label = 'Yearly Mean')
plt.title(f"Yearly Mean Temperature (Slope = {slope:.2f} °C/Year, p = {p_value:.3f})")
plt.xlabel("Year")
plt.ylabel("Temperature (°C)")
plt.show()

monthly_mean = df.groupby(df.index.month)['Mean Temp (°C)'].mean()
monthly_mean.plot(kind = "bar", figsize=(12,5))
plt.title("Average Monthly Temperature")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.show()
