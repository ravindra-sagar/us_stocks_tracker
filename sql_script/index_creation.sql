WITH index_composition AS (
    SELECT 
        mkt_cap.Date,
        mkt_cap.Ticker,
        stocks.Company,
        stocks.Exchange,
        mkt_cap."Adjusted Close",
        mkt_cap."Outstanding Shares" AS "Outstanding Shares",
        (mkt_cap."Adjusted Close" * mkt_cap."Outstanding Shares") AS "Market Capitalization"
    FROM 
        daily_market_cap AS mkt_cap
    LEFT JOIN 
        company_list AS stocks
        ON mkt_cap.Ticker = stocks.Ticker
    WHERE 
        mkt_cap.Date >= current_date - 31
        AND mkt_cap."Adjusted Close" IS NOT NULL
        AND mkt_cap."Outstanding Shares" IS NOT NULL
    QUALIFY 
        ROW_NUMBER() OVER (
            PARTITION BY mkt_cap.Date 
            ORDER BY mkt_cap."Adjusted Close" * mkt_cap."Outstanding Shares" DESC
        ) <= 100)
        
SELECT
    Date,
    SUM("Adjusted Close")/100 AS "Adjusted Close",
    SUM("Outstanding Shares")/100 AS "Outstanding Shares",
    SUM("Market Capitalization")/100 AS "Market Capitalization"
FROM 
    index_composition
GROUP BY 
    Date
ORDER BY
    Date DESC;