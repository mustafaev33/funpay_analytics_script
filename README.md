[🇺 Читать на русском](README_RU.md) | [🇬🇧 Read in English](README.md)

# FunPay Analytics Script

A Python script for automatic collection, structuring, and analysis of sales data from the FunPay marketplace.

Solves the problem of lacking built-in analytics on the platform, helping sellers turn raw transaction data into clear financial reports and visualizations.

## Key Features

- **Auto Cookie Collection**: automatically extracts session cookies from the browser — no manual copying required.
- **Smart CSV Updating**: appends only new sales, ignoring duplicates by order ID.
- **Localization**: supports both Russian and English interfaces.
- **Text Analytics**: automatic calculation of revenue, average order value, refund rate, and sales by period.
- **Visualization**: generates clean charts (revenue trends, deal status distribution).

## Tech Stack

Built in **Python** using a mix of procedural and modular approaches (functions, loops, separate modules).

**Libraries used:**
- `Pandas` — data cleaning, transformation, and analysis.
- `BeautifulSoup4` & `requests` — HTML parsing and HTTP requests.
- `browser_cookie3` — secure cookie extraction from browsers.
- `matplotlib` — chart and diagram rendering.
- `dateparser` — intelligent Russian-language date parsing.

## Installation & Usage

*(This section will be updated after packaging the script into a standalone .exe file for easy use without Python installed).*

## Examples

### Working with the Script
![Language Selection](screenshots/lang_select.png)
*Figure 1: Language selection for script usage*

![Cookie Collection](screenshots/cookie_collect.png)
*Figure 2: Cookie collection option (auto-mode or manual input)*

![Save to CSV](screenshots/save_to_csv.png)
*Figure 3: Option to save data in convenient CSV format table*

### Analytics Output
![Choose Analytics](screenshots/analytics_choose.png)
*Figure 4: Option to run analytics on collected data*

![Analytics](screenshots/analytics_stats.png)
*Figure 5: Analytics summary from collected data*

![Date/Time Analytics](screenshots/datetime_stats.png)
*Figure 6: Monthly and weekly sales analytics from collected data*

### Charts & Visualizations
![Charts and Diagrams](screenshots/visual.png)
*Figure 7: Generated charts and pie diagrams showing key metrics*