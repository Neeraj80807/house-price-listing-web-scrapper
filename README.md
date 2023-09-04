# Housing.com Price Listing Web Scraper using python and BeautifulSoup

This Python script allows you to scrape real estate data from [Housing.com](https://housing.com) and save it into an Excel file. It extracts information about residential projects, builders, project details, configurations, amenities, and more.

## Prerequisites

Before using the script, make sure you have the following:

- Python 3.x installed on your system.
- The required libraries installed. You can install them using pip:

```bash
pip install requests pandas beautifulsoup4
```

## How to Use

1. Clone this repository to your local machine or download the script directly.

```bash
git clone https://github.com/your-username/housing-com-scraper.git
```

2. Open the terminal and navigate to the project folder.

```bash
cd housing-com-scraper
```

3. Edit the script to set your target URL:

```python
# URL of the webpage
url = "https://housing.com/in/buy/searches/AE0P38f9yfbk7p3m2h1f"
```

4. Run the script:

```bash
python main_runner.py
```

5. The script will start scraping data from the specified URL and save it to an Excel file named `project_data.xlsx`.

## Script Structure

- `main_runner.py`: The main Python script for scraping data from Housing.com.
- `main_runner.ipynb`: The interactive python notebook for scraping data from Housing.com.
- `README.md`: This file, providing instructions on how to use the script.

## Output

The script will generate an Excel file (`project_data.xlsx`) containing detailed information about the scraped real estate projects, including project name, pricing, configurations, builder details, and more.

## Disclaimer

This script is provided for educational and research purposes only. Please ensure that you comply with Housing.com's terms of use and policies when using this script. The authors of this script are not responsible for any misuse or violation of Housing.com's terms.

## License

This script is licensed under the [MIT License](LICENSE). Feel free to modify and use it as needed.
