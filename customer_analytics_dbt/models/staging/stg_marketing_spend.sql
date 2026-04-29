-- stg_marketing_spend.sql
-- author: Connor Dailey
-- date: 2026-04-29
-- description: staging view over raw_marketing_spend; basis for CAC calculations

SELECT
    spend_id,
    channel,
    spend_date,
    amount_usd,
    campaign_name
FROM {{ source('raw', 'raw_marketing_spend') }}