
-- 1. Total net revenue

SELECT
    SUM(
        CASE
            WHEN LOWER(TRIM(CAST(o.returned AS TEXT))) IN ('yes', 'true', '1')
                THEN 0
            ELSE o.quantity * o.unit_price * (1 - o.discount)
        END
    ) AS total_net_revenue
FROM orders o
WHERE o.order_date IS NOT NULL
  AND o.quantity > 0
  AND o.unit_price > 0
  AND o.discount BETWEEN 0 AND 1;


-- 2. Top 10 customers

SELECT
    c.customer_name,
    c.city,
    COUNT(DISTINCT o.order_id) AS number_of_orders,
    SUM(
        CASE
            WHEN LOWER(TRIM(CAST(o.returned AS TEXT))) IN ('yes', 'true', '1')
                THEN 0
            ELSE o.quantity * o.unit_price * (1 - o.discount)
        END
    ) AS total_spending
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_date IS NOT NULL
  AND o.quantity > 0
  AND o.unit_price > 0
  AND o.discount BETWEEN 0 AND 1
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spending DESC
LIMIT 10;


-- 3. Category-wise revenue

SELECT
    p.category,
    SUM(
        CASE
            WHEN LOWER(TRIM(CAST(o.returned AS TEXT))) IN ('yes', 'true', '1')
                THEN 0
            ELSE o.quantity * o.unit_price * (1 - o.discount)
        END
    ) AS revenue,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(o.quantity) AS quantity_sold
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
WHERE o.order_date IS NOT NULL
  AND o.quantity > 0
  AND o.unit_price > 0
  AND o.discount BETWEEN 0 AND 1
GROUP BY p.category
ORDER BY revenue DESC;


-- 4. Monthly net revenue

SELECT
    strftime('%Y-%m', o.order_date) AS month,
    SUM(
        CASE
            WHEN LOWER(TRIM(CAST(o.returned AS TEXT))) IN ('yes', 'true', '1')
                THEN 0
            ELSE o.quantity * o.unit_price * (1 - o.discount)
        END
    ) AS net_revenue
FROM orders o
WHERE o.order_date IS NOT NULL
  AND o.quantity > 0
  AND o.unit_price > 0
  AND o.discount BETWEEN 0 AND 1
GROUP BY strftime('%Y-%m', o.order_date)
ORDER BY month;


-- 5. Top 5 products

SELECT
    p.product_name,
    p.category,
    SUM(
        CASE
            WHEN LOWER(TRIM(CAST(o.returned AS TEXT))) IN ('yes', 'true', '1')
                THEN 0
            ELSE o.quantity * o.unit_price * (1 - o.discount)
        END
    ) AS net_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
WHERE o.order_date IS NOT NULL
  AND o.quantity > 0
  AND o.unit_price > 0
  AND o.discount BETWEEN 0 AND 1
GROUP BY p.product_id, p.product_name, p.category
ORDER BY net_revenue DESC
LIMIT 5;

