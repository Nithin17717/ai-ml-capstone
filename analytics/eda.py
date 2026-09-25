import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("MODULE 2 - TITANIC DATASET")

# TASK 1: LOAD TITANIC DATASET

df = sns.load_dataset("titanic")

print("\nDataset loaded successfully.")

# Immediately save the raw dataset
df.to_csv("titanic.csv", index=False)

print("Raw dataset saved as: titanic.csv")

# DATASET INFO

print("DATASET INFO")

df.info()

# DATASET DESCRIPTION

print("DATASET DESCRIPTION")

print(df.describe(include="all"))

# DATASET SHAPE

print("DATASET SHAPE")

print(df.shape)

# MISSING VALUE PERCENTAGES

print("MISSING VALUE PERCENTAGES")

missing_percentage = df.isnull().mean() * 100

missing_percentage = (
    missing_percentage[missing_percentage > 0]
    .sort_values(ascending=False)
)

print(missing_percentage)

# TASK 2: HANDLE MISSING VALUES

print("TASK 2 - MISSING VALUE HANDLING")

print("\nMissing percentage for affected columns:")

for column in missing_percentage.index:
    print(f"{column}: {missing_percentage[column]:.2f}%")

# Under 5% -> drop rows
rows_before = len(df)

df = df.dropna(subset=["embarked", "embark_town"])

rows_after = len(df)

print("\nRows dropped because embarked/embark_town missing:")
print(rows_before - rows_after)

# 5% - 30% -> impute
age_median = df["age"].median()

df["age"] = df["age"].fillna(age_median)

print(f"\nAge missing values imputed using median: {age_median:.2f}")

# More than 30% -> drop column
df = df.drop(columns=["deck"])

print("\nDropped column: deck")
print("Reason: 77.22% of its values were missing.")

# VERIFY CLEANED DATA

print("CLEANED DATASET")

print(f"Shape after cleaning: {df.shape}")

print("\nRemaining missing values:")

remaining_missing = df.isnull().sum()
remaining_missing = remaining_missing[remaining_missing > 0]

if remaining_missing.empty:
    print("No missing values remain.")
else:
    print(remaining_missing)

# Save cleaned dataset
df.to_csv("titanic.csv", index=False)

print("\nCleaned dataset saved to titanic.csv")

# TASK 3: DISTRIBUTIONS AND OUTLIERS

print("TASK 3 - DISTRIBUTIONS AND OUTLIERS")

# Create charts folder
import os

os.makedirs("charts", exist_ok=True)

# AGE HISTOGRAM

plt.figure(figsize=(8, 5))
plt.hist(df["age"], bins=20, edgecolor="black")
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("charts/age_histogram.png")
plt.close()

# AGE BOXPLOT

plt.figure(figsize=(8, 4))
plt.boxplot(df["age"])
plt.title("Age Box Plot")
plt.ylabel("Age")
plt.tight_layout()
plt.savefig("charts/age_boxplot.png")
plt.close()

# FARE HISTOGRAM

plt.figure(figsize=(8, 5))
plt.hist(df["fare"], bins=20, edgecolor="black")
plt.title("Fare Distribution")
plt.xlabel("Fare")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("charts/fare_histogram.png")
plt.close()

# FARE BOXPLOT

plt.figure(figsize=(8, 4))
plt.boxplot(df["fare"])
plt.title("Fare Box Plot")
plt.ylabel("Fare")
plt.tight_layout()
plt.savefig("charts/fare_boxplot.png")
plt.close()

print("\nCharts saved:")
print("charts/age_histogram.png")
print("charts/age_boxplot.png")
print("charts/fare_histogram.png")
print("charts/fare_boxplot.png")

# IQR OUTLIER CALCULATION

def calculate_iqr_outliers(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = series[
        (series < lower_bound) |
        (series > upper_bound)
    ]

    return q1, q3, iqr, lower_bound, upper_bound, len(outliers)


age_q1, age_q3, age_iqr, age_lower, age_upper, age_outliers = (
    calculate_iqr_outliers(df["age"])
)

fare_q1, fare_q3, fare_iqr, fare_lower, fare_upper, fare_outliers = (
    calculate_iqr_outliers(df["fare"])
)

print("AGE IQR OUTLIERS")

print(f"Q1: {age_q1:.2f}")
print(f"Q3: {age_q3:.2f}")
print(f"IQR: {age_iqr:.2f}")
print(f"Lower bound: {age_lower:.2f}")
print(f"Upper bound: {age_upper:.2f}")
print(f"Outlier count: {age_outliers}")

print("FARE IQR OUTLIERS")

print(f"Q1: {fare_q1:.2f}")
print(f"Q3: {fare_q3:.2f}")
print(f"IQR: {fare_iqr:.2f}")
print(f"Lower bound: {fare_lower:.2f}")
print(f"Upper bound: {fare_upper:.2f}")
print(f"Outlier count: {fare_outliers}")

# FARE MEAN, MEDIAN AND MODE

fare_mean = df["fare"].mean()
fare_median = df["fare"].median()
fare_mode = df["fare"].mode().iloc[0]

print("FARE SUMMARY")

print(f"Mean: {fare_mean:.2f}")
print(f"Median: {fare_median:.2f}")
print(f"Mode: {fare_mode:.2f}")

# SKEWNESS CONCLUSION

print("FARE SKEWNESS")

if fare_mean > fare_median > fare_mode:
    print("Fare is positively (right) skewed.")
    print("Reason: Mean > Median > Mode.")
elif fare_mean < fare_median < fare_mode:
    print("Fare is negatively (left) skewed.")
    print("Reason: Mean < Median < Mode.")
else:
    print("Fare does not follow a simple mean-median-mode skewness ordering.")

# TASK 4: SURVIVAL RATES AND CORRELATION

print("TASK 4 - SURVIVAL RATES AND CORRELATION")

# SURVIVAL RATE BY SEX

print("SURVIVAL RATE BY SEX")

male_passengers = df[df["sex"] == "male"]
female_passengers = df[df["sex"] == "female"]

male_survival_rate = male_passengers["survived"].mean() * 100
female_survival_rate = female_passengers["survived"].mean() * 100

print(f"Male survival rate: {male_survival_rate:.2f}%")
print(f"Female survival rate: {female_survival_rate:.2f}%")

# SURVIVAL RATE BY PASSENGER CLASS

print("SURVIVAL RATE BY PASSENGER CLASS")

for pclass in sorted(df["pclass"].unique()):
    class_passengers = df[df["pclass"] == pclass]
    survival_rate = class_passengers["survived"].mean() * 100

    print(
        f"Class {pclass} survival rate: "
        f"{survival_rate:.2f}%"
    )

# SURVIVAL RATE BY SEX + PASSENGER CLASS

print("SURVIVAL RATE BY SEX + PASSENGER CLASS")

for sex in ["female", "male"]:
    for pclass in sorted(df["pclass"].unique()):

        group = df[
            (df["sex"] == sex) &
            (df["pclass"] == pclass)
        ]

        survival_rate = group["survived"].mean() * 100

        print(
            f"{sex.capitalize()}, Class {pclass}: "
            f"{survival_rate:.2f}%"
        )

# CORRELATION MATRIX
print("CORRELATION MATRIX")

correlation_columns = [
    "survived",
    "pclass",
    "age",
    "sibsp",
    "parch",
    "fare"
]

correlation_matrix = df[correlation_columns].corr()

print(correlation_matrix.round(3))

# CORRELATION HEATMAP

plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title("Titanic Feature Correlation Heatmap")
plt.tight_layout()

plt.savefig("charts/correlation_heatmap.png")
plt.close()

print("\nCorrelation heatmap saved:")
print("charts/correlation_heatmap.png")

# TWO STRONGEST ABSOLUTE OFF-DIAGONAL CORRELATIONS

correlation_pairs = []

for i in range(len(correlation_columns)):
    for j in range(i + 1, len(correlation_columns)):

        column_1 = correlation_columns[i]
        column_2 = correlation_columns[j]

        correlation_value = correlation_matrix.loc[
            column_1,
            column_2
        ]

        correlation_pairs.append(
            (
                column_1,
                column_2,
                correlation_value,
                abs(correlation_value)
            )
        )

correlation_pairs.sort(
    key=lambda x: x[3],
    reverse=True
)

print("TWO STRONGEST ABSOLUTE OFF-DIAGONAL CORRELATIONS")

for column_1, column_2, value, absolute_value in correlation_pairs[:2]:

    print(
        f"{column_1} <-> {column_2}: "
        f"{value:.3f} "
        f"(absolute = {absolute_value:.3f})"
    )

# TASK 5: ADDITIONAL VISUALIZATIONS

print("TASK 5 - ADDITIONAL VISUALIZATIONS")

# CHART 1: SURVIVAL RATE BY SEX

sex_survival = df.groupby("sex", observed=True)["survived"].mean() * 100

plt.figure(figsize=(7, 5))
sex_survival.plot(kind="bar")

plt.title("Survival Rate by Sex")
plt.xlabel("Sex")
plt.ylabel("Survival Rate (%)")
plt.xticks(rotation=0)
plt.ylim(0, 100)

plt.tight_layout()
plt.savefig("charts/survival_by_sex.png")
plt.close()

print("Created: charts/survival_by_sex.png")

# CHART 2: SURVIVAL RATE BY PASSENGER CLASS

class_survival = df.groupby("pclass", observed=True)["survived"].mean() * 100

plt.figure(figsize=(7, 5))
class_survival.plot(kind="bar")

plt.title("Survival Rate by Passenger Class")
plt.xlabel("Passenger Class")
plt.ylabel("Survival Rate (%)")
plt.xticks(rotation=0)
plt.ylim(0, 100)

plt.tight_layout()
plt.savefig("charts/survival_by_class.png")
plt.close()

print("Created: charts/survival_by_class.png")

# CHART 3: SURVIVAL RATE BY SEX + CLASS

sex_class_survival = (
    df.groupby(["sex", "pclass"], observed=True)["survived"]
    .mean()
    .unstack()
    * 100
)

plt.figure(figsize=(8, 5))
sex_class_survival.plot(kind="bar")

plt.title("Survival Rate by Sex and Passenger Class")
plt.xlabel("Sex")
plt.ylabel("Survival Rate (%)")
plt.xticks(rotation=0)
plt.ylim(0, 100)
plt.legend(title="Passenger Class")

plt.tight_layout()
plt.savefig("charts/survival_by_sex_class.png")
plt.close()

print("Created: charts/survival_by_sex_class.png")

# CHART 4: AGE DISTRIBUTION BY SURVIVAL STATUS

plt.figure(figsize=(8, 5))

survived_age = df[df["survived"] == 1]["age"]
not_survived_age = df[df["survived"] == 0]["age"]

plt.hist(
    [not_survived_age, survived_age],
    bins=20,
    label=["Did Not Survive", "Survived"],
    alpha=0.7
)

plt.title("Age Distribution by Survival Status")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.legend()

plt.tight_layout()
plt.savefig("charts/age_by_survival.png")
plt.close()

print("Created: charts/age_by_survival.png")

# TASK 5 INTERPRETATIONS

print("TASK 5 - CHART INTERPRETATIONS")

print("""
Chart 1 - Survival Rate by Sex:
Female passengers had a substantially higher survival rate than male
passengers in the cleaned Titanic dataset. The survival rates were
74.04% for females and 18.89% for males.

Chart 2 - Survival Rate by Passenger Class:
Survival rate decreased as passenger class increased from Class 1 to
Class 3. Class 1 had a survival rate of 62.62%, compared with 24.24%
for Class 3.

Chart 3 - Survival Rate by Sex and Passenger Class:
Survival rates varied across both sex and passenger class. Female
passengers had higher survival rates than male passengers within
each passenger class, while the rates also differed between classes.

Chart 4 - Age Distribution by Survival Status:
The age distributions of passengers who survived and those who did not
overlap across several age ranges. The chart shows that both groups
contained passengers across a wide range of ages.
""")

# SAVE CHART INTERPRETATIONS

interpretations = """
# Task 5 - Chart Interpretations

## Chart 1 - Survival Rate by Sex

Female passengers had a substantially higher survival rate than male
passengers in the cleaned Titanic dataset. The survival rates were
74.04% for females and 18.89% for males.

## Chart 2 - Survival Rate by Passenger Class

Survival rate decreased as passenger class increased from Class 1 to
Class 3. Class 1 had a survival rate of 62.62%, compared with 24.24%
for Class 3.

## Chart 3 - Survival Rate by Sex and Passenger Class

Survival rates varied across both sex and passenger class. Female
passengers had higher survival rates than male passengers within
each passenger class, while the rates also differed between classes.

## Chart 4 - Age Distribution by Survival Status

The age distributions of passengers who survived and those who did not
overlap across several age ranges. The chart shows that both groups
contained passengers across a wide range of ages.
"""

with open("task5_interpretations.md", "w", encoding="utf-8") as file:
    file.write(interpretations)

print("\nTask 5 interpretations saved to task5_interpretations.md")

# TASK 6: Z-SCORE STANDARDIZATION

print("TASK 6 - Z-SCORE STANDARDIZATION")

# Use the full cleaned DataFrame for exploratory standardization.
# This standardized data will NOT be used for modeling.

age_mean_before = df["age"].mean()
age_std_before = df["age"].std()

fare_mean_before = df["fare"].mean()
fare_std_before = df["fare"].std()

print("\nBEFORE STANDARDIZATION")
print("-" * 70)

print(f"Age   - Mean: {age_mean_before:.4f}, Std: {age_std_before:.4f}")
print(f"Fare  - Mean: {fare_mean_before:.4f}, Std: {fare_std_before:.4f}")

# Calculate z-scores
df["age_zscore"] = (
    (df["age"] - df["age"].mean())
    / df["age"].std()
)

df["fare_zscore"] = (
    (df["fare"] - df["fare"].mean())
    / df["fare"].std()
)

age_mean_after = df["age_zscore"].mean()
age_std_after = df["age_zscore"].std()

fare_mean_after = df["fare_zscore"].mean()
fare_std_after = df["fare_zscore"].std()

print("\nAFTER STANDARDIZATION")
print("-" * 70)

print(
    f"Age z-score   - Mean: {age_mean_after:.6f}, "
    f"Std: {age_std_after:.6f}"
)

print(
    f"Fare z-score  - Mean: {fare_mean_after:.6f}, "
    f"Std: {fare_std_after:.6f}"
)

print("\nConclusion:")
print(
    "After z-score standardization, Age and Fare have means "
    "approximately equal to 0 and standard deviations approximately equal to 1."
)

print(
    "These standardized columns are for exploratory analysis only "
    "and will not be used as the modeling input."
)