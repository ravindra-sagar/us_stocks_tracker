WITH index_composition AS (
    SELECT 
        mkt_cap.Date,
        mkt_cap.Ticker,
        stocks.Company,
        stocks.Exchange,
        mkt_cap."Adjusted Close",
        mkt_cap."Outstanding Shares",
        (mkt_cap."Adjusted Close" * mkt_cap."Outstanding Shares") AS "Market Capitalization",
        ROW_NUMBER() OVER (
            PARTITION BY mkt_cap.Date 
            ORDER BY mkt_cap."Adjusted Close" * mkt_cap."Outstanding Shares" DESC
        ) AS Rank
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
),

current_index_composition AS (
    SELECT 
        Date,
        Ticker,
        Rank
    FROM 
        index_composition
),

previous_index_composition AS (
    SELECT 
        Date,
        LAG(Ticker) OVER(PARTITION BY Rank ORDER BY Date) AS Ticker,
        Rank
    FROM 
        current_index_composition
),

composition_change AS (
    SELECT
        curr.Date,
        SUM(CASE 
                WHEN prev.Ticker IS NULL THEN 1
                ELSE 0
            END) AS change_in_composition
    FROM 
        current_index_composition curr
    LEFT JOIN 
        previous_index_composition prev
        ON curr.Date = prev.Date 
        AND curr.Ticker = prev.Ticker
    GROUP BY 
        curr.Date
),


daily_index_price AS (
    SELECT
        Date,
        SUM("Adjusted Close")/100 AS Price
    FROM 
        index_composition
    GROUP BY 
        Date
),


base_index_price AS (
    SELECT 
        Date,
        Price
    FROM 
        daily_index_price
    WHERE 
        Date = (
            SELECT MIN(Date) 
            FROM daily_index_price
        )
),

previous_day_index_price AS (
    SELECT
        Date,
        LAG(Price) OVER(ORDER BY Date) AS Price
    FROM daily_index_price
)


-- Final selection: compare the ticker lists for each date
SELECT
    cc.Date,
    CASE 
        WHEN cc.Date = bip.Date THEN 'Base Date'
        WHEN cc.change_in_composition > 0 THEN 'Yes' 
        ELSE 'No' 
    END AS "Change in Composition",
    CASE 
        WHEN cc.Date = bip.Date THEN 0
        ELSE cc.change_in_composition 
    END AS "No of Changes in Composition",
    -- Cumulative Return %
    ROUND((dip.Price - bip.Price)/bip.Price * 100, 2) AS "Cumulative Return %",
    -- Daily Return %
    ROUND((dip.Price - pdip.Price)/pdip.Price * 100, 2) AS "Daily Return %"
FROM 
    composition_change cc
LEFT JOIN 
    daily_index_price dip ON cc.Date = dip.Date
CROSS JOIN 
    base_index_price bip 
LEFT JOIN 
    previous_day_index_price pdip ON cc.Date = pdip.Date
ORDER BY 
    cc.Date DESC;

