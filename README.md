[🇺 Читать на русском](README_RU.md) | [🇬🇧 Read in English](README.md)

<p align="center">
  <img src="screenshots/logo.png" alt="FunPay Analytics Logo" width="250"/>
</p>

# FunPay Analytics Script by mustafaev33

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
- `rich` — beautiful highlighting of the output text.

## Installation & Usage

You don't need to install Python or any libraries. The tool is packaged in a ZIP archive with all dependencies.

### 1. Download
Go to the [Releases](https://github.com/mustafaev33/funpay_analytics_script/releases) page and download the latest archive `FunPayAnalytics_v1.1.0.zip`.

### 2. Unpacking
Unzip the archive to any convenient folder (for example, `C:\Programs\FunPayAnalytics`).

### 3. First Launch & Windows Defender
Since the `.exe` is not digitally signed, Windows SmartScreen or your antivirus might show a warning.
- Click **"More info"** -> **"Run anyway"**.
- Alternatively, add the folder with the `.exe` to your antivirus exclusions.

### 4. How to use
1. Run `FunPayAnalytics.exe`.
2. Choose your language (`ru` / `en`).
3. Enter your FunPay sales page URL (or press Enter for default).
4. Choose cookie collection method (Auto or Manual).
5. Follow the on-screen prompts to save data, run analytics, and view charts.

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

## Contact & Feedback

Found a bug? Have a feature request?
- **Issues:** Open an issue on [GitHub](https://github.com/mustafaev33/funpay_analytics_script/issues)
- **Telegram:** [@mustafaev33](https://t.me/mustafaev33)
- **Email:** rdd22833t@gmail.com
- **FunPay** [FunPay](https://funpay.com/users/2671110/)