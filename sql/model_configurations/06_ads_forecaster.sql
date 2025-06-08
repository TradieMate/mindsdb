-- Google Ads Revenue Forecasting Model
-- Time-series model for predicting future ad performance

CREATE MODEL mindsdb.ads_forecaster
FROM supabase_analytics
  (SELECT 
    date,
    campaign_id,
    daily_revenue,
    daily_clicks,
    daily_impressions,
    daily_conversions,
    daily_cost
   FROM daily_ad_performance
   WHERE daily_revenue IS NOT NULL)
PREDICT daily_revenue
USING 
  engine = 'lightwood',
  tag = 'ads revenue forecasting',
  time_column = 'date',
  order_by = 'date',
  window = 30,  -- Use 30 days of historical data
  horizon = 7,  -- Predict 7 days ahead
  group_by = 'campaign_id';