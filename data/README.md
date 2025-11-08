# Data Directory

This directory contains the student survey data used for training the recommendation model.

## Files

- `students.csv` - Main dataset with student preferences and characteristics

## Data Schema

The dataset includes the following key features:

### Numerical Features
- `teamwork_preference` (1-5): Preference for working in teams
- `introversion_extraversion` (1-5): Personality scale (1=introvert, 5=extrovert)
- `books_read_past_year` (int): Number of books read annually
- `weekly_hobby_hours` (float): Hours spent on hobbies per week
- `risk_taking` (1-5): Risk-taking tendency
- `conscientiousness` (1-5): Conscientiousness level
- `open_to_new_experiences` (1-5): Openness to new experiences

### Categorical Features
- `club_top1`, `club_top2`: Primary and secondary club memberships
- `hobby_top1`, `hobby_top2`: Primary and secondary hobbies

## Data Privacy

- All data is anonymized
- No personally identifiable information (PII) is stored
- Student IDs are system-generated indices

## Usage

```python
import pandas as pd

# Load data
df = pd.read_csv('data/students.csv')
print(df.shape)
print(df.columns)
```
