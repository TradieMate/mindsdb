# Model Query Examples

This directory contains example queries for using the analytics optimization models.

## Getting Predictions

### Google Ads Optimization
```sql
-- Get revenue predictions for new ad configurations
SELECT 
  predicted_revenue,
  confidence,
  ad_text,
  time_of_day,
  bid_amount
FROM mindsdb.google_ads_optimizer
WHERE 
  click_through_rate = 0.05
  AND audience_segment = 'high-intent'
  AND device_type = 'mobile';
```

### Website Conversion Optimization
```sql
-- Get conversion rate predictions for page improvements
SELECT 
  predicted_conversion_rate,
  confidence,
  page_load_time,
  traffic_source,
  device_type
FROM mindsdb.website_conversion_optimizer
WHERE 
  bounce_rate < 0.3
  AND session_duration > 120
  AND pages_per_session > 2;
```

### Customer Journey Value Prediction
```sql
-- Predict customer lifetime value
SELECT 
  predicted_customer_lifetime_value,
  confidence,
  first_touch_channel,
  touchpoint_count
FROM mindsdb.customer_journey_optimizer
WHERE 
  email_opens > 5
  AND website_visits > 3;
```

### Ad Text Performance
```sql
-- Test new ad text variations
SELECT 
  predicted_click_through_rate,
  confidence,
  ad_headline,
  sentiment_score
FROM mindsdb.ad_text_performance
WHERE 
  ad_headline = 'New Product Launch - 50% Off!'
  AND call_to_action = 'Shop Now';
```

### Revenue Forecasting
```sql
-- Get 7-day revenue forecast
SELECT 
  predicted_daily_revenue,
  confidence,
  date,
  campaign_id
FROM mindsdb.ads_forecaster
WHERE 
  campaign_id = 'campaign_123'
  AND date > LATEST;
```

## Environment Variables

Set these environment variables for Supabase connection:
- `SUPABASE_USER`: Your Supabase database user
- `SUPABASE_PASSWORD`: Your Supabase database password  
- `SUPABASE_HOST`: Your Supabase project host (e.g., xyz.supabase.co)
- `SUPABASE_PORT`: Your Supabase port (usually 5432)
- `SUPABASE_DATABASE`: Your Supabase database name (usually postgres)

Additional required variables:
- `OPENAI_API_KEY`: Required for AI/ML features
- `MINDSDB_DEFAULT_LLM_API_KEY`: Default LLM API key (often same as OpenAI)