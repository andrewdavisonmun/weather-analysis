#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 13:44:25 2025

@author: andrewdavison
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from function import daily_temperature_range, rolling_mean_temperature, yearly_extreme_days, yearly_mean_temperature, temperature_trend, get_season
import calendar

df = pd.read_csv("toronto_citycentre_daily_2005_2025.csv")

df["Date/Time"] = pd.to_datetime(df["Date/Time"], errors="coerce")

df = df.dropna(subset=["Date/Time"])

df = df[(df["Date/Time"] >= "2005-01-01") & (df["Date/Time"] <= "2025-12-31")]

df = df.sort_values("Date/Time")

df = df[df["Date/Time"] >= "2011-01-01"]

df = df.set_index("Date/Time")

for col in ["Max Temp (°C)", "Min Temp (°C)", "Mean Temp (°C)"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

sns.set_palette("colorblind")
sns.set_style("whitegrid")
sns.set_palette("colorblind")

y_min = df["Min Temp (°C)"].min() - 2
y_max = df["Max Temp (°C)"].max() + 2

# Plot Daily Max/Min Temp
plt.figure(figsize=(12,5))
plt.plot(df.index, df["Max Temp (°C)"], color="orangered", alpha=0.7, label="Max Temp")
plt.plot(df.index, df["Min Temp (°C)"], color="skyblue", alpha=0.7, label="Min Temp")

plt.title("Toronto City Centre — Daily Temperatures (2011–2025)", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Temperature (°C)", fontsize=12)
plt.legend()
plt.grid(True, alpha = 0.3)
plt.ylim(y_min, y_max)

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Plot Daily Temperature Range
df["Temp_Range"] = daily_temperature_range(df)

plt.figure(figsize=(12,5))
plt.plot(df.index, df["Temp_Range"], color = 'purple', alpha = 0.7, label="Daily Temp Range")
plt.title("Daily Temperature Range (Max - Min)", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Temperature Range (°C)", fontsize=12)
plt.grid(True, alpha = 0.3)
plt.legend()

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# Plot Rolling Mean Temperature
df["Rolling_Mean"] = rolling_mean_temperature(df, window = 30)
plt.figure(figsize=(12,5))
plt.plot(df.index, df["Mean Temp (°C)"], color = 'grey', alpha = 0.4, label = 'Daily Mean')
plt.plot(df.index, df["Rolling_Mean"], color = "orange", linewidth = 2, label = '30-Day Rolling Mean')
plt.title("Toronto Mean Temperature with 30-Day Rolling Average", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Temperature (°C)", fontsize=12)
plt.legend()

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.xticks(rotation=0)

plt.grid(True, alpha = 0.3)
plt.ylim(y_min, y_max)
plt.tight_layout()
plt.show()

# Plot Yearly Extreme Hot and Cold Days
yearly_extremes = yearly_extreme_days(df)
yearly_extremes.plot(kind = "bar", figsize = (12,5), color = ['orangered', 'skyblue'])
plt.title("Yearly Extreme Hot and Cold Days", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number of Extreme Days", fontsize=12)
plt.xticks(rotation = 0)
plt.grid(axis = 'y', alpha = 0.3)
plt.legend(['Extreme Hot Days','Extreme Cold Days'])
plt.tight_layout()
plt.show()

# Plot Yearly Mean Temp with Trend
yearly_mean = yearly_mean_temperature(df)
slope, p_value = temperature_trend(yearly_mean.index, yearly_mean.values)

yearly_mean_dt = pd.to_datetime(yearly_mean.index.astype(str) + "-01-01")
plt.figure(figsize=(12,5))
plt.plot(yearly_mean_dt, yearly_mean.values, marker = 'o', color = 'green', label = 'Yearly Mean')
plt.title(f"Yearly Mean Temperature (Slope = {slope:.2f} °C/Year, p = {p_value:.3f})", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Mean Temperature (°C)", fontsize=12)
plt.grid(True, alpha = 0.3)

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# Plot Average Monthly Temp
monthly_mean = df.groupby(df.index.month)['Mean Temp (°C)'].mean()
monthly_mean.plot(kind = "bar", figsize=(12,5), color = 'teal', label = 'Avg Temp')
plt.title("Average Monthly Temperature", fontsize=16)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Temperature (°C)", fontsize=12)
plt.xticks(ticks=range(12), labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], rotation=0)
plt.grid(axis = 'y', alpha = 0.3)
plt.legend()
plt.tight_layout()
plt.show()

# Plot Heatmap

df['Year'] = df.index.year
df['DayOfYear'] = df.index.dayofyear
pivot_temp = df.pivot_table(values='Mean Temp (°C)', index='Year', columns='DayOfYear')

plt.figure(figsize=(15,6))
sns.heatmap(pivot_temp, cmap='coolwarm', cbar_kws={'label': 'Mean Temperature (°C)'}, xticklabels=False)

month_starts = [pd.Timestamp(f'2020-{m:02d}-01').dayofyear for m in range(1,13)]
month_names = [calendar.month_abbr[m] for m in range(1,13)]
plt.xticks(ticks=[m-1 for m in month_starts], labels=month_names, rotation=0)

plt.title("Daily Mean Temperature Heatmap (2011–2025)", fontsize=16)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Year", fontsize=12)
plt.tight_layout()
plt.show()

# Plot Season

df["Season"] = df.index.month.map(get_season)

seasonal_mean = df.groupby('Season')['Mean Temp (°C)'].mean()
season_order = ['Winter', 'Spring', 'Summer', 'Fall']

plt.figure(figsize=(10,5))
seasonal_mean = seasonal_mean.reindex(season_order)
bars = plt.bar(seasonal_mean.index, seasonal_mean.values, color=['skyblue','green','orangered','gold'])

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.09, f"{height:.1f}", ha='center', va='bottom', fontsize=12)
    
plt.title("Average Temperature by Season", fontsize=16)
plt.xlabel("Season", fontsize=12)
plt.ylabel("Mean Temperature (°C)", fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
