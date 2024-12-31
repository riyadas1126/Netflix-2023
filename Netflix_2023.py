import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set display options for better readability
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

# Import the dataset
file_path = '/mnt/data/netflix_content_2023.csv'
df = pd.read_csv(file_path)

# Display the first few rows and dataset information
df.head()
df.info()

# Data Cleaning: Replace commas in 'Hours Viewed' and convert to float
df['Hours Viewed'] = df['Hours Viewed'].replace(',', '', regex=True).astype(float)

# Preview titles with their viewership hours
df[['Title', 'Hours Viewed']].head()

# Visualization 1: Viewership by Content Type
viewership = df.groupby('Content Type')['Hours Viewed'].sum()
plt.figure(figsize=(12, 8))
plt.bar(viewership.index, viewership.values)
plt.title('Total Viewership Hours by Content Type (Shows vs Movies)')
plt.xlabel('Content Type')
plt.ylabel('Total Hours Viewed (in billions)')
plt.show()

# Visualization 2: Viewership by Language Indicator
Language_viewership = df.groupby('Language Indicator')['Hours Viewed'].sum().sort_values(ascending=False)
plt.figure(figsize=(12, 8))
plt.bar(Language_viewership.index, Language_viewership.values)
plt.title('Total Viewership Hours by Language 2023')
plt.xlabel('Language Indicator')
plt.ylabel('Total Hours Viewed (in billions)')
plt.show()

# Convert 'Release Date' to datetime format and extract the month
df['Release Date'] = pd.to_datetime(df['Release Date'])
df['Release Month'] = df['Release Date'].dt.month

# Visualization 3: Monthly Viewership Trend
monthly_viewership = df.groupby('Release Month')['Hours Viewed'].sum()
plt.figure(figsize=(12, 8))
plt.plot(monthly_viewership.index, monthly_viewership.values, marker='o', linestyle='-')
plt.title('Monthly Viewership Trend in 2023')
plt.xlabel('Month')
plt.ylabel('Total Hours Viewed (in billions)')
plt.xticks(range(1, 13))
plt.grid(True)
plt.tight_layout()
plt.show()

# Identify Top 5 Titles by Viewership
top_5_titles = df.nlargest(5, 'Hours Viewed')
top_5_titles[['Title', 'Hours Viewed']]

# Visualization 4: Monthly Viewership Trends by Content Type
viewership_trends = df.groupby(['Release Month', 'Content Type'])['Hours Viewed'].sum().unstack()
plt.figure(figsize=(10, 6))
for content_type in viewership_trends.columns:
    plt.plot(viewership_trends.index, viewership_trends[content_type], marker='o', label=content_type)
plt.title('Monthly Viewership Trends by Content Type')
plt.xlabel('Month')
plt.ylabel('Total Hours Viewed (in billions)')
plt.xticks(range(1, 13))
plt.legend(title='Content Type')
plt.grid(True)
plt.tight_layout()
plt.show()

# Function to categorize seasons based on month
def get_season(month):
    if month in (12, 1, 2):
        return 'Winter'
    elif month in (3, 4, 5):
        return 'Spring'
    elif month in (6, 7, 8):
        return 'Summer'
    else:
        return 'Fall'

# Create 'Season' column
df['Season'] = df['Release Month'].apply(get_season)

# Visualization 5: Viewership by Season
seasonal_viewership = df.groupby('Season')['Hours Viewed'].sum()
seasonal_viewership = seasonal_viewership.reindex(['Winter', 'Spring', 'Summer', 'Fall'])
plt.figure(figsize=(8, 6))
plt.bar(seasonal_viewership.index, seasonal_viewership.values)
plt.title('Total Viewership Hours by Season')
plt.xlabel('Season')
plt.ylabel('Total Hours Viewed (in billions)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Visualization 6: Monthly Content Releases and Viewership Comparison
monthly_releases = df['Release Month'].value_counts().sort_index()
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(monthly_releases.index, monthly_releases.values, alpha=0.6, label='Number of Releases')
ax1.set_xlabel('Month')
ax1.set_ylabel('Number of Releases', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_xticks(range(1, 13))
ax1.set_title('Monthly Content Releases and Viewership Hours')

ax2 = ax1.twinx()
ax2.plot(monthly_viewership.index, monthly_viewership.values, color='orange', marker='o', label='Viewership Hours')
ax2.set_ylabel('Total Hours Viewed (in billions)', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

ax1.grid(axis='y', linestyle='--', alpha=0.7)
fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.show()

# Visualization 7: Releases and Viewership by Weekday
df['Weekday'] = df['Release Date'].dt.day_name()
weekday_releases = df['Weekday'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
weekday_viewership = df.groupby('Weekday')['Hours Viewed'].sum().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(weekday_releases.index, weekday_releases.values, alpha=0.6, label='Number of Releases', color='skyblue')
ax1.set_xlabel('Weekday')
ax1.set_ylabel('Number of Releases', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_title('Content Releases and Viewership Hours by Weekday')

ax2 = ax1.twinx()
ax2.plot(weekday_viewership.index, weekday_viewership.values, color='orange', marker='o', label='Viewership Hours')
ax2.set_ylabel('Total Hours Viewed (in billions)', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

ax1.grid(axis='y', linestyle='--', alpha=0.7)
fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.show()

# Holiday Analysis
holidays = [
    '2023-01-01', '2023-02-14', '2023-07-04', '2023-10-31', '2023-12-25'
]
holidays = pd.to_datetime(holidays)
holiday_releases = df[df['Release Date'].apply(lambda x: any((x - date).days in range(-3, 4) for date in holidays))]
holiday_viewership = holiday_releases.groupby('Release Date')['Hours Viewed'].sum()

# Display holiday releases with viewership
holiday_releases[['Title', 'Release Date', 'Hours Viewed']]
