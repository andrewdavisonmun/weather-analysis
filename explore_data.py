#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 13:54:43 2025

@author: andrewdavison
"""

import pandas as pd

df = pd.read_csv("~/Downloads/weather_data/toronto_citycentre_daily_2005_2025.csv")

df["Date/Time"] = pd.to_datetime(df["Date/Time"], errors="coerce")
df = df.dropna(subset=["Date/Time"])
df = df.set_index("Date/Time").sort_index()

df.describe().T

high_cutoff = df["Max Temp (°C)"].quantile(0.99)
low_cutoff  = df["Min Temp (°C)"].quantile(0.01)

extreme_hot = df[df["Max Temp (°C)"] >= high_cutoff]
extreme_cold = df[df["Min Temp (°C)"] <= low_cutoff]

print(f"Extreme hot days: {len(extreme_hot)}")
print(f"Extreme cold days: {len(extreme_cold)}")

missing_per_year = df.isna().groupby(df.index.year).sum()
print(missing_per_year.head())