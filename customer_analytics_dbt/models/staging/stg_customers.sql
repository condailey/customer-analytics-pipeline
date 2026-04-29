-- stg_customers.sql
-- author: Connor Dailey
-- date: 2026-04-29
-- description: staging view over raw_customers; passes columns through for downstream models

SELECT
    customer_id,
    company_name,
    plan_tier,
    signup_date,
    industry,
    company_size,
    acquisition_channel
FROM {{ source('raw', 'raw_customers') }}