import pandas as pd

df = pd.read_json("data/trends_20260924.json")

print("Original rows:", len(df))
print(df.head())

print(df.info())
print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate post IDs:")
print(df["post_id"].duplicated().sum())

df = df.drop_duplicates(subset="post_id")

print("After removing duplicates:", len(df))

df = df.dropna(
    subset=["post_id", "title", "score"]
)

print("After removing missing values:", len(df))

df["score"] = pd.to_numeric(
    df["score"],
    errors="coerce"
)

df["num_comments"] = pd.to_numeric(
    df["num_comments"],
    errors="coerce"
)

df["score"] = df["score"].fillna(0).astype(int)

df["num_comments"] = (
    df["num_comments"]
    .fillna(0)
    .astype(int)
)

df = df[df["score"] >= 5]
print("After score filtering:", len(df))

df["title"] = df["title"].str.strip()
df.to_csv(
    "data/trends_clean.csv",
    index=False
)
print("Cleaned data saved successfully!")

print("\nFinal row count:", len(df))
print("\nStories per category:")
print(df["category"].value_counts())
print("\nCleaned data saved to:")
print("data/trends_clean.csv")