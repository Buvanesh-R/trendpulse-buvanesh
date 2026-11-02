# TrendPulse

TrendPulse is a small data pipeline that collects trending stories from **Hacker News**, cleans them, analyses engagement by topic, and produces charts. It is split into four scripts that are run one after another, each reading the output of the previous one.

## What it does

1. **Collects** top stories from the Hacker News API and sorts them into five topic categories using keyword matching.
2. **Cleans** the collected data (removes duplicates and missing values, fixes data types, filters out low-scoring stories).
3. **Analyses** the cleaned data (score and comment statistics, engagement, per-category summary).
4. **Visualises** the results as three charts saved as PNG images.

## Categories

Stories are assigned to the first category whose keywords appear in the title:

| Category | Example keywords |
|---|---|
| `technology` | ai, software, programming, github, python, linux, cloud |
| `worldnews` | war, election, government, president, ukraine, china, india |
| `sports` | football, cricket, tennis, nba, olympics, premier league |
| `science` | science, research, nasa, space, physics, climate |
| `entertainment` | movie, film, music, netflix, gaming, hollywood |

Up to 25 stories are kept per category, so the raw dataset has at most 125 stories.

## Project structure

```
trendpulse-buvanesh/
├── task1_data_collection.py   # Fetch + categorise Hacker News stories -> JSON
├── task2_data_processing.py   # Clean the JSON -> CSV
├── task3_analysis.py          # Statistics and category summary -> CSV
├── task4_visualization.py     # Charts -> PNG
├── data/                      # Raw, cleaned, and analysis data files
└── outputs/                   # Generated charts
```

## Tech stack

- Python 3
- [requests](https://pypi.org/project/requests/) for calling the Hacker News API
- [pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/) for cleaning and analysis
- [Matplotlib](https://matplotlib.org/) for charts

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Buvanesh-R/trendpulse-buvanesh.git
cd trendpulse-buvanesh
```

### 2. Install dependencies

```bash
pip install requests pandas numpy matplotlib
```

### 3. Run the pipeline in order

```bash
python task1_data_collection.py
python task2_data_processing.py
python task3_analysis.py
python task4_visualization.py
```

> **Note:** `task2_data_processing.py` currently reads a fixed file name, `data/trends_20260924.json`. After running Task 1 on a new day, update that file name in Task 2 to match the new `data/trends_YYYYMMDD.json` file that was created.

## Pipeline details

### Task 1: Data collection (`task1_data_collection.py`)

- Calls `https://hacker-news.firebaseio.com/v0/topstories.json` for the list of top story IDs.
- Fetches the first 500 stories one by one from the item endpoint, skipping any request that fails.
- Categorises each story by title keywords and keeps at most 25 per category.
- Saves the result to `data/trends_YYYYMMDD.json`.

Each saved record contains:

| Field | Description |
|---|---|
| `post_id` | Hacker News story ID |
| `title` | Story title |
| `category` | One of the five categories above |
| `score` | Upvote score |
| `num_comments` | Number of comments |
| `author` | Username of the submitter |
| `collected_at` | UTC timestamp of collection |

### Task 2: Data processing (`task2_data_processing.py`)

- Loads the raw JSON into a pandas DataFrame.
- Removes duplicate `post_id` values and rows missing `post_id`, `title`, or `score`.
- Converts `score` and `num_comments` to integers (invalid values become 0).
- Keeps only stories with a **score of 5 or more**.
- Trims whitespace from titles.
- Saves the result to `data/trends_clean.csv`.

### Task 3: Analysis (`task3_analysis.py`)

- Prints the average score and comments, plus mean, median, standard deviation, maximum, and minimum of the score.
- Finds the most common category and the most commented story.
- Computes `engagement` (score + comments) and flags a story as popular when its score is at or above the median.
- Builds a per-category summary (story count, average score, average comments) and saves it to `data/trends_analysis.csv`.

### Task 4: Visualisation (`task4_visualization.py`)

Creates three charts in `outputs/`:

| File | Chart |
|---|---|
| `chart1_top_stories.png` | Horizontal bar chart of the top 10 stories by score |
| `chart2_categories.png` | Bar chart of the number of stories per category |
| `chart3_scatter.png` | Scatter plot of score vs comments, popular vs non-popular |

## Output files

| File | Created by |
|---|---|
| `data/trends_YYYYMMDD.json` | Task 1 |
| `data/trends_clean.csv` | Task 2 |
| `data/trends_analysis.csv` | Task 3 |
| `outputs/chart1_top_stories.png` | Task 4 |
| `outputs/chart2_categories.png` | Task 4 |
| `outputs/chart3_scatter.png` | Task 4 |

## Known limitations and ideas for improvement

- **Keyword matching is simple.** Keywords are matched as substrings of the title, and the first matching category wins, so short keywords like `ai` or `us` can match inside longer words. Matching whole words (for example with regular expressions) would be more accurate.
- **Task 2 uses a hard-coded input file name** (see the note above). Reading the newest `trends_*.json` file automatically would remove the manual edit.
- **Task 1 contains exploratory test code** (printing the first story and testing the categoriser) that runs before the main collection loop and could be removed or moved into a separate test.
- Story fetching is sequential, so collecting 500 stories takes a while. Using concurrent requests would speed it up.

## Author

Buvanesh R ([@Buvanesh-R](https://github.com/Buvanesh-R))

## Data source

Story data comes from the public [Hacker News API](https://github.com/HackerNews/API).
