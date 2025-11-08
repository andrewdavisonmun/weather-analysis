#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 13:44:25 2025

@author: andrewdavison
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv("~/Downloads/weather_data/toronto_citycentre_daily_2005_2025.csv")

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
