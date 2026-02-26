-- select all transaction with symbol EURUSD
SELECT s.symbolname, o.direction, o.volume FROM orders o
JOIN symbol s ON o.symbolid = s.symbolid
WHERE s.symbolname = 'EURUSD';

-- validate transaction
WITH sum_volume AS (
    SELECT
        SUM(
            o.volume *
            CASE
                WHEN o.direction = 'BUY' THEN 1
                ELSE -1
            END
        ) AS total_volume
    FROM orders o
    JOIN symbol s ON o.symbolid = s.symbolid
    WHERE s.symbolname = 'EURUSD'
)
SELECT
    CASE
        WHEN total_volume < 0 THEN 'SELL'
        ELSE 'BUY'
    END AS direction,
    ABS(total_volume) AS total_volume
FROM sum_volume;

-- Answer: the direction and total volume is correct