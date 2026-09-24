import pandas as pd
import matplotlib.pyplot as plt
import os

print("TASK 4 STARTED")

# Load cleaned data
df = pd.read_csv("data/trends_clean.csv")

# Create outputs folder
os.makedirs("outputs", exist_ok=True)


# ==========================================
# CHART 1: Top 10 Stories by Score
# Horizontal Bar Chart
# ==========================================

top_stories = df.nlargest(10, "score")

plt.figure(figsize=(10, 6))

plt.barh(
    top_stories["title"],
    top_stories["score"]
)

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story")

plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("outputs/chart1_top_stories.png")
plt.close()


# ==========================================
# CHART 2: Number of Stories by Category
# Bar Chart
# ==========================================

category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 6))

plt.bar(
    category_counts.index,
    category_counts.values
)

plt.title("Number of Stories by Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("outputs/chart2_categories.png")
plt.close()


# ==========================================
# CHART 3: Score vs Comments
# Popular vs Non-Popular
# Scatter Plot
# ==========================================

# Define popular stories using median score
median_score = df["score"].median()

df["is_popular"] = df["score"] >= median_score

popular = df[df["is_popular"] == True]
non_popular = df[df["is_popular"] == False]

plt.figure(figsize=(9, 6))

plt.scatter(
    non_popular["score"],
    non_popular["num_comments"],
    label="Non-Popular"
)

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

plt.legend()

plt.tight_layout()

plt.savefig("outputs/chart3_scatter.png")
plt.close()


print("\nTASK 4 COMPLETED SUCCESSFULLY!")

print("\nCharts saved:")
print("outputs/chart1_top_stories.png")
print("outputs/chart2_categories.png")
print("outputs/chart3_scatter.png")