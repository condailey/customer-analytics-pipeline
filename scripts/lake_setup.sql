-- lake_setup.sql
-- author: Connor Dailey
-- date: 2026-04-29
-- description: bootstraps the snowflake data lake with database, schemas, and raw tables

-- Database holds all pipeline state across raw, staging, and analytics layers
CREATE OR REPLACE DATABASE CUSTOMER_ANALYTICS;

USE CUSTOMER_ANALYTICS;

-- Schemas correspond to dbt model layers
CREATE OR REPLACE SCHEMA RAW;
CREATE OR REPLACE SCHEMA STAGING;
CREATE OR REPLACE SCHEMA ANALYTICS;

-- Customer dimension, populated from CSV via Snowsight load
CREATE OR REPLACE TABLE RAW.raw_customers (
    customer_id VARCHAR PRIMARY KEY,
    company_name VARCHAR,
    plan_tier VARCHAR,
    signup_date DATE,
    industry VARCHAR,
    company_size VARCHAR,
    acquisition_channel VARCHAR
);

-- Subscription lifecycle events (signup, churn, etc.); mrr_change drives revenue marts
CREATE OR REPLACE TABLE RAW.raw_subscription_events (
    event_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    event_type VARCHAR,
    event_date DATE,
    old_plan VARCHAR,
    new_plan VARCHAR,
    mrr_change NUMBER(10,2)
);

-- Weekly marketing spend per channel; feeds CAC calculations
CREATE OR REPLACE TABLE RAW.raw_marketing_spend (
    spend_id VARCHAR PRIMARY KEY,
    channel VARCHAR,
    spend_date DATE,
    amount_usd NUMBER(10,2),
    campaign_name VARCHAR
);

-- Support tickets; resolved_date is null when ticket is still open
CREATE OR REPLACE TABLE RAW.raw_support_tickets (
    ticket_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    created_date DATE,
    resolved_date DATE,
    priority VARCHAR,
    category VARCHAR
);