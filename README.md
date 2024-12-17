# US Stocks Tracker

## **Overview**
This project builds a data pipeline that tracks the performance of a custom equal-weighted stock index of the top 100 US companies by market capitalization. The pipeline collects, processes, and visualizes data while providing export functionalities for further analysis.

---

## **Features**

- **Data Collection**: Fetches daily adjusted closing prices of US stocks using Alpha Vantage and Yahoo Finance APIs.
- **Data Storage**: Stores the collected data in a DuckDB database for efficient querying.
- **Custom Index Calculation**: Computes the performance of an equal-weighted custom stock index with dynamic composition based on market prices.
- **Dashboard**:
  - Visualizes price performance and index composition.
  - Displays key metrics, such as daily and cumulative returns.
- **Export Capabilities**:
  - Generates PDF and Excel reports summarizing the index performance and composition.

---

## **Technology Stack**

| **Technology**           | **Purpose**                          |
|--------------------------|--------------------------------------|
| Python, SQL              | Core programming languages           |
| Alpha Vantage, yfinance  | Stock market data retrieval          |
| requests                 | HTTP requests for API interactions   |
| DuckDB                   | In-Memory Database                   |
| pandas                   | Data analysis and manipulation       |
| datetime                 | Date and time operations             |
| FPDF                     | PDF file generation                  |
| Dash                     | Interactive dashboard and UI         |
| Plotly                   | Data visualization library           |

---

## **Setup Instructions**

### **Prerequisites**
- Python 3.8 or above
- pip (Python package installer)

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/ravindra-sagar/us_stocks_tracker.git
   cd us_stocks_tracker
   ```
2. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**

1. Run the pipeline:
   ```bash
   python main.py
   ```

2. Access the dashboard at:
   [http://127.0.0.1:8050](http://127.0.0.1:8050)

3. PDF and Excel outputs will be available in the `output_YYYYMMDD` directory, where `YYYYMMDD` is the current date.

---

## **Future Improvements**

- **Advanced Analytics**: Incorporate sectoral analysis, volatility metrics, and sentiment analysis.
- **Real-time Updates**: Enable live data visualization and tracking.
- **Enhanced Data Sources**: Integrate alternative datasets like news, earnings, or macroeconomic indicators.
- **Performance Optimization**: Implement caching for faster data retrieval and processing.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.
