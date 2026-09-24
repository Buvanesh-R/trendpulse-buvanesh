import pandas as pd
import numpy as np

print("TASK 3 STARTED")

# Load cleaned data
df = pd.read_csv("data/trends_clean.csv")

print("Total stories:", len(df))

# Average metrics
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

# Descriptive statistics
mean_score = df["score"].mean()
median_score = df["score"].median()
std_score = df["score"].std()
max_score = df["score"].max()
min_score = df["score"].min()

# Most common category
most_common_category = df["category"].value_counts().idxmax()

# Most commented story
most_commented = df.loc[df["num_comments"].idxmax()]

# Engagement
df["engagement"] = df["score"] + df["num_comments"]

# Popular stories
df["is_popular"] = np.where(
    df["score"] >= df["score"].median(),
    True,
    False
)

# Category summary
category_summary = df.groupby("category").agg(
    stories=("post_id", "count"),
    average_score=("score", "mean"),
    average_comments=("num_comments", "mean")
).reset_index()

category_summary["average_score"] = category_summary["average_score"].round(2)
category_summary["average_comments"] = category_summary["average_comments"].round(2)

# Save analysis results
category_summary.to_csv(
    "data/trends_analysis.csv",
    index=False
)

# Display results
print("\n--- Average Metrics ---")
print("Average score:", round(average_score, 2))
print("Average comments:", round(average_comments, 2))

print("\n--- Score Statistics ---")
print("Mean:", round(mean_score, 2))
print("Median:", round(median_score, 2))
print("Standard deviation:", round(std_score, 2))
print("Maximum:", max_score)
print("Minimum:", min_score)

print("\n--- Most Common Category ---")
print(most_common_category)

print("\n--- Most Commented Story ---")
print("Title:", most_commented["title"])
print("Comments:", most_commented["num_comments"])
print("Category:", most_commented["category"])

print("\n--- Category Summary ---")
print(category_summary)

print("\nAnalysis saved to: data/trends_analysis.csv")
print("TASK 3 COMPLETED SUCCESSFULLY!")