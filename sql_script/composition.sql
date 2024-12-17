SELECT 
    mkt_cap.Date,
    mkt_cap.Ticker,
    stocks.Company,
    stocks.Exchange,
    ROUND(mkt_cap."Adjusted Close", 2) AS "Adjusted Close (In USD)",
    ROUND(mkt_cap."Outstanding Shares" / 1000000, 2) AS "Outstanding Shares (In Million)",
    ROUND((mkt_cap."Adjusted Close" * mkt_cap."Outstanding Shares") / 1000000000, 2) AS "Market Capitalization (In Billion USD)"
FROM 
    daily_market_cap AS mkt_cap
LEFT JOIN 
    company_list AS stocks
    ON mkt_cap.Ticker = stocks.Ticker
WHERE 
    mkt_cap.Date >= CURRENT_DATE - 31
    AND mkt_cap."Adjusted Close" IS NOT NULL
    AND mkt_cap."Outstanding Shares" IS NOT NULL
QUALIFY 
    ROW_NUMBER() OVER (
        PARTITION BY mkt_cap.Date 
        ORDER BY mkt_cap."Adjusted Close" * mkt_cap."Outstanding Shares" DESC
    ) <= 100
ORDER BY 
    mkt_cap."Adjusted Close" * mkt_cap."Outstanding Shares" DESC;
