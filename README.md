# ⛳ Golf Maps & Analysis: End-to-End Data Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python >=3.13](https://img.shields.io/badge/python-%3E%3D3.13-blue.svg)](https://www.python.org/) [![pandas >=2.3.3](https://img.shields.io/badge/pandas-%3E%3D2.3.3-blue.svg)](https://pypi.org/project/pandas/) [![plotly >=6.5.0](https://img.shields.io/badge/plotly-%3E%3D6.5.0-blue.svg)](https://pypi.org/project/plotly/) [![dash >=3.3.0](https://img.shields.io/badge/dash-%3E%3D3.3.0-blue.svg)](https://pypi.org/project/dash/) [![pydantic >=2.12.5](https://img.shields.io/badge/pydantic-%3E%3D2.12.5-blue.svg)](https://pypi.org/project/pydantic/) [![dash-bootstrap-components >=2.0.4](https://img.shields.io/badge/dash--bootstrap--components-%3E%3D2.0.4-blue.svg)](https://pypi.org/project/dash-bootstrap-components/)

**A production-grade ETL pipeline and interactive Dash application for personal golf performance tracking and analysis.**

An end-to-end Python application that ingests personal golf scorecard data, enriches it with geolocation via the Google Maps API, validates it through Pydantic schemas, and delivers actionable performance insights through an interactive web dashboard — including an interactive map of every course played.

- [⛳ Golf Maps \& Analysis: End-to-End Data Pipeline](#-golf-maps--analysis-end-to-end-data-pipeline)
  - [🎯 Project Objective](#-project-objective)
  - [⚙️ The Data Pipeline](#️-the-data-pipeline)
  - [📊 Visualization \& UI](#-visualization--ui)
  - [✨ Features](#-features)
  - [📥 Installation](#-installation)
    - [Option 1: Using `uv` (Recommended)](#option-1-using-uv-recommended)
    - [Option 2: Using Python venv + pip](#option-2-using-python-venv--pip)
  - [⚙️ Configuration](#️-configuration)
    - [Google Maps API Key](#google-maps-api-key)
    - [Adding Your Data File](#adding-your-data-file)
  - [📂 Project Structure](#-project-structure)
  - [📋 Sample Data Format](#-sample-data-format)
    - [Golf Courses Sheet](#golf-courses-sheet)
    - [Rounds Sheet](#rounds-sheet)
  - [🚀 Usage](#-usage)
  - [Data Validation \& Error Logging](#data-validation--error-logging)
    - [Row-Level Error Tracking](#row-level-error-tracking)
    - [Example Error Output](#example-error-output)
    - [Error Logging Logic](#error-logging-logic)
  - [🎨 Dashboard Overview](#-dashboard-overview)
    - [**Course Map**](#course-map)
    - [**Score Trends**](#score-trends)
    - [**Course Deep-Dive**](#course-deep-dive)
  - [🛠️ Requirements](#️-requirements)
    - [🐍 Python Environment](#-python-environment)
    - [📦 Key Dependencies](#-key-dependencies)
  - [🧪 Running Tests](#-running-tests)
  - [📜 License](#-license)
  - [🤝 Contributing](#-contributing)


## 🎯 Project Objective

The primary goal of this project is to demonstrate a **production-grade Python workflow** applied to personal sports analytics. It serves as a blueprint for an end-to-end process: taking raw, manually logged scorecard data through a structured ETL pipeline — leveraging functional programming, external API enrichment, and Pydantic validation — and delivering actionable insights via an interactive web dashboard.

This data from this project is based on data the author has collected over the last 10 years. 

## ⚙️ The Data Pipeline

The core logic is divided into five distinct stages to ensure data integrity and modularity:

1. **Data Loading:** Ingesting raw golf course and rounds data from a source Excel file using `python-calamine` for fast parsing.
2. **Data Cleaning:** Normalising dates, handling missing values, and standardising column types for consistent downstream processing.
3. **Geocoding:** Enriching each golf course record with latitude/longitude coordinates via the **Google Maps API**, enabling map-based visualisation.
4. **Pydantic Validation (v2.12):** Enforcing strict schemas across three models — `GolfCourse`, `GolfRounds`, and `RoundPerformance` — to ensure the pipeline remains robust and type-safe. Invalid records are captured and logged rather than silently dropped.
5. **Data Transformation:** Aggregating validated records into analytical datasets — round summaries, course summaries, performance summaries, and average performance metrics — ready for the dashboard.

The **`DataPipeline`** modules orchestrate this flow, leveraging **Pandas** for high-performance transformations and **Pydantic** for rigorous schema enforcement.

## 📊 Visualization & UI

The processed data is served through a **Plotly Dash** interface. By utilising **Plotly Express** and **Plotly Graph Objects**, the project generates interactive visualisations that allow users to:

* Explore every course played on an interactive map
* Monitor scoring trends, rolling averages, and performance bands over time
* Break down performance by individual skill area at a per-course level

Application styling and layout are developed with **Dash Bootstrap Components**.

## ✨ Features

- Interactive map of all courses played, geocoded via the Google Maps API
- Score trend analysis with rolling average, rolling best, and rolling worst
- Course-level performance breakdown across five skill dimensions: Driving, Irons, Inside 100 Yards, Chipping, and Putting
- Per-course round history table, filterable by course
- Pydantic-validated data pipeline with graceful error logging for invalid records
- Support for both 9-hole and 18-hole rounds via adjusted score normalisation


## 📥 Installation

### Option 1: Using `uv` (Recommended)

```bash
git clone <repository-url>
cd Golf-maps-and-analysis
uv sync
```

### Option 2: Using Python venv + pip

```bash
git clone <repository-url>
cd Golf-maps-and-analysis
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e .
```

## <a name="configuration"></a>⚙️ Configuration

### Google Maps API Key

This project uses the **Google Maps Geocoding API** to resolve golf course addresses to coordinates. You will need a valid API key to run the geocoding step.

Create a `.env` file in the project root:

```env
GOOGLE_MAPS_API_KEY="your_api_key_here"
```

To obtain a key, follow the [Google Maps Platform quickstart](https://developers.google.com/maps/get-started). The Geocoding API is the only Maps service required.

### Adding Your Data File

Place your golf rounds Excel file in the `data/` folder. By default the pipeline expects:

```
data/golf rounds.xlsx
```

The file must contain two sheets: `golf courses` (starting at row 4, columns B–M) and `Rounds` (starting at row 3, columns B–AG). See [Sample Data Format](#-sample-data-format) for the full schema.

## 📂 Project Structure

Within the repo sits the following structure:

- `src/` contains
    - `app/` — Dash app factory with Plotly charts and interactive dashboard pages
    - `models/` — Pydantic data schemas (`GolfCourse`, `GolfRounds`, `RoundPerformance`)
    - `pipeline/` — ETL orchestration modules: `data_handler`, `data_processing`, `data_transformation`, `data_validation`, `geocoding`
- `tests/` — Unit tests
- `main.py` — Execution entry point

## 📋 Sample Data Format

The pipeline expects an `.xlsx` file with two sheets, structured as follows:

### Golf Courses Sheet

| Column | Type | Example |
| :--- | :--- | :--- |
| `Course Name` | string | Woldingham Golf Club |
| `Address` | string | Halliloo Valley Rd |
| `Post Code` | string (str dtype) | CR3 7HA |
| `Par` | integer | 71 |

### Rounds Sheet

| Column | Type | Example |
| :--- | :--- | :--- |
| `Round Number` | integer | 75 |
| `Course` | string | Park Wood |
| `Played with` | string | Chris, Mark |
| `Date` | date | 2023-04-10 |
| `Year` | integer | 2023 |
| `Format` | string | Stroke Play |
| `Score` | integer | 103 |
| `Holes` | integer | 18 |
| `Par` | integer | 72 |
| `Over Par` | integer | 31 |
| `Adj 18 hole over par` | float | 31.0 |
| `Adj 18 hole over par, post course adjustment` | float | 26.78 |
| `Overall Performance` | string | Only hit half swings... |
| `Adj Rolling Average` | float | 28.24 |
| `Rolling Average` | float | 29.8 |
| `Driving` | integer (1–10) | 9 |
| `Duff Drives` | float | 0 |
| `Irons` | integer (1–10) | 8 |
| `Inside 100 Yards` | integer (1–10) | 5 |
| `Chipping` | integer (1–10) | 5 |
| `Shots Lost In Bunkers` | integer | 0 |
| `Putting` | integer (1–10) | 7 |
| `Duff Shots` | integer | 2 |
| `Triple Bogeys` | integer | 3 |
| `Driving comments` | string | Struck the ball well |
| `Iron comments` | string | Half swings were good |
| `Inside 100 yard comments` | string | Hit one duff full wedge |
| `Chipping Comments` | string | Hit a few thin shots |
| `Bunker Comments` | string | Got out of 2 bunkers well |
| `Putting comments` | string | Generally quite good |

**Skill ratings** (Driving, Irons, Inside 100 Yards, Chipping, Putting) are scored on a **1–10 scale**.

**Supported formats:** `Stroke Play`

Place your rounds file in the `data/` folder (`.xlsx` format):

```bash
data/golf rounds.xlsx
```

## 🚀 Usage

Run the data pipeline and launch the interactive dashboard:

```bash
python main.py
```

Run with `uv`:

```bash
uv run python main.py
```

The dashboard will be available at `http://127.0.0.1:8052` by default.

> **Note:** A valid `GOOGLE_MAPS_API_KEY` in your `.env` file is required on first run to geocode the courses. Subsequent runs may cache results depending on your setup.

## Data Validation & Error Logging

The pipeline employs a **"Graceful Failure"** strategy for data validation using Pydantic. When records fail validation (e.g., missing fields, incorrect data types, or out-of-range skill ratings), they are not silently dropped. Instead, they are captured, formatted, and stored in a dedicated error DataFrame.

Three Pydantic models govern the validation:

- **`GolfCourse`** — validates course-level data including geocoded coordinates
- **`GolfRounds`** — validates round-level data including scores, dates, and format
- **`RoundPerformance`** — validates the 1–10 skill ratings and shot-level commentary

### Row-Level Error Tracking

For every record that triggers a `ValidationError`, the pipeline:

1. **Extracts the raw record data** — keeps the original values for context
2. **Counts the issues** — records the total number of validation failures for that row
3. **Formats error details** — concatenates multiple errors into a numbered, readable list identifying exactly which field failed and why

### Example Error Output

If the pipeline encounters invalid data, the resulting `error_df` will be structured as follows:

| Course | Score | Driving | ... | total_errors | error_details |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Park Wood | "None" | 9 | ... | 2 | 1) Score: input is not a valid integer <br> 2) Date: field required |
| Woldingham | 89 | 15 | ... | 1 | 1) Driving: value must be less than or equal to 10 |

### Error Logging Logic

The following pattern in `data_validation.py` ensures that every validation failure is documented:

```python
except ValidationError as e:
    # Format multiple errors into a single string for the record
    details = "\n".join(
        f"{i}) {err['loc'][0]}: {err['msg']}"
        for i, err in enumerate(e.errors(), 1)
    )

    # Append the original record + error metadata to the error list
    error_records.append({
        **record_dict,
        'total_errors': e.error_count(),
        'error_details': details
    })

# Convert to DataFrame for review / export
error_df = pd.DataFrame(error_records)
```

## 🎨 Dashboard Overview

The dashboard provides three views for analysing golf performance across all rounds and courses played:

### **Course Map**

A geographic overview of every course in your history, plotted on an interactive Plotly map.

* **Geocoded course markers:** Each course is pinned using coordinates resolved via the Google Maps API
* **Course details on hover:** Click or hover over a marker to see course name, location, and summary stats
* **At-a-glance coverage:** Quickly see which courses have been played most frequently and where they're clustered geographically

---

### **Score Trends**

A chronological view of scoring progression, designed to answer the key question: *am I actually getting better?*

* **Rolling average:** Smoothed scoring trend across all rounds, adjusted for 9 vs 18 holes
* **Rolling best & worst:** Banded view showing the trajectory of peak and poor rounds over time
* **Key performance metrics:** Summary KPIs including overall average, best round, and most recent score — all normalised to an 18-hole equivalent over-par basis

---

### **Course Deep-Dive**

A granular breakdown of performance at a specific course, selectable via a dropdown.

* **Skill radar / bar chart:** Average performance ratings across five dimensions — Driving, Irons, Inside 100 Yards, Chipping, and Putting — for all rounds at the selected course versus the average across all courses
* **Round history table:** Full log of every round played at the selected course, including date, score, over par
* **Course-adjusted benchmarking:** Scores are normalised relative to course par and difficulty adjustment, enabling fair comparison across different venues

## 🛠️ Requirements

To run this project, you will need the following environment and dependencies:

### 🐍 Python Environment

* **Python 3.13+**: This project utilises recent Python features and optimisations.
* **uv**: It is recommended to use [uv](https://github.com/astral-sh/uv) for dependency synchronisation and virtual environment management.
* **Google Maps API Key**: Required for the geocoding step. See [Configuration](#️-configuration).

### 📦 Key Dependencies

| Dependency | Version | Purpose |
| :--- | :--- | :--- |
| **Pydantic** | `>=2.12.5` | Data validation and schema enforcement using Python type hints |
| **Dash** | `>=3.3.0` | Framework for building the analytical web dashboard |
| **Plotly** | `>=6.5.0` | Interactive data visualisations including maps and charts |
| **Pandas** | `>=2.3.3` | High-performance data manipulation and transformation |
| **googlemaps** | `>=4.10.0` | Google Maps Geocoding API client for course address enrichment |
| **pydantic-settings** | `>=2.12.0` | Settings management via environment variables |
| **pydantic-extra-types** | `>=2.11.0` | Additional Pydantic type validators (e.g., country codes) |
| **pycountry** | `>=24.6.1` | ISO country code lookup, used in address validation |
| **python-calamine** | `>=0.6.1` | Fast Excel file reading engine |
| **openpyxl** | `>=3.1.5` | Excel file writing for report exports |
| **Dash Bootstrap Components** | `>=2.0.4` | Bootstrap components for Plotly Dash styling |
| **Pytest** | `>=9.0.2` | Testing framework for validating pipeline logic |

## 🧪 Running Tests

Run all unit tests using:

```bash
# Using uv
uv run pytest

# Or using Python directly (if venv is activated)
python -m pytest
```

## 📜 License

Distributed under the **MIT License**. See [LICENSE.txt](LICENSE.txt) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue to discuss proposed changes.
