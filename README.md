# weather-analysis

# Toronto Weather Data Analysis (2011-2025)

This project explores daily weather measurements from station Toronto City Centre in the years from 2011 to 2025.

- **explore_data.py** - data cleaning and exploration
- **plots.py** - visualization of temperature
- **function.py** - functions
- **test_functions.py** - test

The data used is uploaded in the repository as:
"toronto_citycentre_daily_2005_2025.csv"

## 1. exploredata.py - Data Exploration and Cleaning
- Loads data
- Cleans "Date/Time" column
- Computes descriptive statistics
- Identifies extreme hot and cold days using percentiles
- Counts missing values

## 2. plots.py - Temperature Visualization
- Uses Matplotlib
- Daily maximum, minimum, and mean temperatures
- Daily temperature ranges
- Rolling mean temperatures
- Yearly extreme hot and cold days
- Yearly mean temperatures and trends
- Seasonal temperature patterns
- Monthly temperature patterns
- Daily mean temperature heatmap

## 3. function.py - functions
- daily_temperature_range(df) – calculates daily temperature range
- rolling_mean_temperature(df, window=30) – computes rolling mean temperatures
- yearly_extreme_days(df, high_quantile=0.99, low_quantile=0.01) – counts yearly extreme hot and cold days
- yearly_mean_temperature(df) – calculates yearly mean temperatures
- temperature_trend(years, values) – calculates linear trend of yearly mean temperatures
- get_season(month) – maps month number to season

## 4. test_functions.py - tests
- tests the functions in function.py

To run the plots
on terminal:
# Clone the repository
git clone https://github.com/andrewdavisonmun/weather-analysis.git
cd weather-analysis
# Install dependencies
pip install -r requirements.txt
# Run the plots
python plots.py
