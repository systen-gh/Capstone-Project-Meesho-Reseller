CREATE TABLE IF NOT EXISTS reseller_mask_map (
    reseller_id TEXT PRIMARY KEY,
    masked_reseller_id TEXT UNIQUE
);

INSERT OR IGNORE INTO reseller_mask_map (
    reseller_id,
    masked_reseller_id
)
SELECT
    reseller_id,
    'Reseller_' ||
    printf('%03d',
        ROW_NUMBER() OVER (ORDER BY reseller_id)
    )
FROM (
    SELECT DISTINCT reseller_id
    FROM orders
    WHERE reseller_id IS NOT NULL
);

DROP VIEW IF EXISTS masked_orders;

CREATE VIEW masked_orders AS
SELECT
    o.order_id,
    o.order_date,
    m.masked_reseller_id AS reseller_id,
    o.region,
    o.city,
    o.category,
    o.quantity,
    o.unit_price,
    o.order_amount,
    o.order_status,
    o.revenue
FROM orders AS o
JOIN reseller_mask_map AS m
    ON o.reseller_id = m.reseller_id;