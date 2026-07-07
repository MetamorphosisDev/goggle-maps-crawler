# Google Maps Crawler

A Python-based crawler powered by Playwright for collecting location data from Google Maps using custom search keywords.

The crawler automatically stores results in CSV format and can be customized for various categories such as restaurants, cafés, hotels, schools, pharmacies, gyms, and more.

## Features

* Search Google Maps using custom keywords
* Support multiple cities and regions
* Automatically save results to CSV
* Prevent duplicate URLs
* Built-in logging system
* Easy to customize and extend

## Requirements

* Python 3.10 or higher
* Windows, Linux, or macOS

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd google-maps-crawler
```

### 2. Create a Virtual Environment (Optional)

#### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install pandas playwright beautifulsoup4
```

### 4. Install Playwright Browser

```bash
python -m playwright install chromium
```

## Usage

Run the crawler:

```bash
python crawler.py
```

## Configuration

### Search Keywords

Edit the `KEYWORDS` list:

```python
KEYWORDS = [
    "Restaurant",
    "Cafe",
    "Hotel",
]
```

### Target Locations

Edit the `DATASET_WILAYAH` dictionary:

```python
DATASET_WILAYAH = {
    "West Java": [
        "Depok",
        "Bandung"
    ]
}
```

## Output

### CSV File

The collected data will be saved to:

```text
master_dataset.csv
```

### Log File

Crawler logs will be saved to:

```text
crawler_process.log
```

## Example Use Cases

* Lead generation
* Market research
* Competitor analysis
* Business directory creation
* Location intelligence
* Data collection and analytics

## Troubleshooting

### Playwright Browser Not Found

Run:

```bash
python -m playwright install chromium
```

### Missing Python Modules

Install all required dependencies:

```bash
pip install pandas playwright beautifulsoup4
```

## Disclaimer

Google Maps may change its page structure at any time. If that happens, some selectors used by the crawler may need to be updated for the script to continue working properly.



## Acknowledgements

Special thanks to the original developer(s) whose work served as the foundation of this project.

This repository contains modifications, improvements, and customizations made to fit specific use cases and requirements.

