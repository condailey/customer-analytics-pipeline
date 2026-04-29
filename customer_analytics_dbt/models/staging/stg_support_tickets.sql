-- stg_support_tickets.sql
-- author: Connor Dailey
-- date: 2026-04-29
-- description: staging view over raw_support_tickets; basis for support summary models

SELECT
    ticket_id,
    customer_id,
    created_date,
    resolved_date,
    priority,
    category
FROM {{ source('raw', 'raw_support_tickets') }}