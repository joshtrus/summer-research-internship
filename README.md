# Jamaica Stock Exchange (JSE) Web Scraper

### Author: Josh Morris  
### Date: 07/29/22

## Project Overview

This project is a web scraper designed to collect financial data from the Jamaica Stock Exchange (JSE). It was developed as part of a summer internship, in collaboration with James Karram. The scraper extracts ticker names, article dates, times, summaries, and full articles related to various financial events.

### What the Project Does
- Scrapes all ticker names from the JSE website.
- Extracts financial articles, including the ticker name mentioned, the date and time of publication, a summary, and a full article.
- Stores the scraped data in an SQLite database.
- The scraper is currently configured to retrieve up to 4000 articles, but this can be adjusted.

## How It Works
1. **Ticker Collection**: The scraper first gathers ticker symbols from two indices on the JSE website: the JSE Index and the JSE Select Index.
2. **Article Scraping**: For each news article, the scraper retrieves:
    - Ticker Name
    - Date and Time
    - Article Summary
    - Full Article (if available)
3. **Data Storage**: All the collected data is stored in an SQLite database with two tables: `jse_main` and `jse_select`, corresponding to the two indices.

## Features
- Utilizes `Selenium` to interact with dynamic website content.
- Scrapes data from multiple pages of the news section on the JSE website.
- Stores data in an SQLite database, allowing for easy querying and analysis.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/joshtrus/stock-monitoring-system.git
    cd stock-monitoring-system
    ```

2. **Install Dependencies**:
    Make sure you have `Selenium` installed:
    ```bash
    pip install selenium
    ```

3. **Set Up ChromeDriver**:
    Download ChromeDriver and add its path to your system. Modify the script to point to the correct ChromeDriver path:
    ```python
    os.environ["PATH"] += os.pathsep + r'/path/to/chromedriver'
    ```

4. **Run the Program**:
    ```bash
    python your_scraper_file.py
    ```

## Database Structure

- **jse_main**: Stores the data scraped from the main JSE index.
- **jse_select**: Stores the data scraped from the JSE Select index.

## Future Enhancements
- Scrape article URLs for full-text content.
- Add error handling and logging.
- Automate updates to the database.

## License

This project is open-source and available under the [MIT License](LICENSE).
