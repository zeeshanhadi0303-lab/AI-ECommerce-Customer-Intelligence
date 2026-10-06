-- ============================================================
-- AI POWERED E-COMMERCE CUSTOMER INTELLIGENCE SYSTEM
-- REQUIRED SQL QUERIES
-- ============================================================


-- ============================================================
-- 1. TOTAL NET REVENUE
-- ============================================================

SELECT
    SUM(
        oi.quantity
        * oi.unit_price
        * (1 - COALESCE(oi.discount, 0))
    ) AS total_net_revenue
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
WHERE COALESCE(o.returned, 0) = 0;


-- ============================================================
-- 2. TOP 10 CUSTOMERS BY TOTAL SPENDING
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    SUM(
        oi.quantity
        * oi.unit_price
        * (1 - COALESCE(oi.discount, 0))
    ) AS total_spending
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE COALESCE(o.returned, 0) = 0
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_spending DESC
LIMIT 10;


-- ============================================================
-- 3. CATEGORY REVENUE, ORDER COUNT AND QUANTITY SOLD
-- ============================================================

SELECT
    p.category,
    SUM(
        oi.quantity
        * oi.unit_price
        * (1 - COALESCE(oi.discount, 0))
    ) AS category_revenue,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(oi.quantity) AS quantity_sold
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE COALESCE(o.returned, 0) = 0
GROUP BY p.category
ORDER BY category_revenue DESC;


-- ============================================================
-- 4. MONTHLY NET REVENUE
-- ============================================================

SELECT
    strftime('%Y-%m', o.order_date) AS month,
    SUM(
        oi.quantity
        * oi.unit_price
        * (1 - COALESCE(oi.discount, 0))
    ) AS monthly_net_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE
    COALESCE(o.returned, 0) = 0
    AND o.order_date IS NOT NULL
GROUP BY month
ORDER BY month;


-- ============================================================
-- 5. TOP 5 PRODUCTS BY NET REVENUE
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    SUM(
        oi.quantity
        * oi.unit_price
        * (1 - COALESCE(oi.discount, 0))
    ) AS net_revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE COALESCE(o.returned, 0) = 0
GROUP BY
    p.product_id,
    p.product_name
ORDER BY net_revenue DESC
LIMIT 5;