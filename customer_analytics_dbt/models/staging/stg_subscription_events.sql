-- stg_subscription_events.sql
-- author: Connor Dailey
-- date: 2026-04-29
-- description: staging view over raw_subscription_events; basis for MRR and churn marts

SELECT
    event_id,
    customer_id,
    event_type,
    event_date,
    old_plan,
    new_plan,
    mrr_change
FROM {{ source('raw', 'raw_subscription_events') }}