-- Google Ads Revenue Optimization Model
-- Predicts revenue based on ad performance metrics

CREATE MODEL mindsdb.google_ads_optimizer
FROM supabase_analytics
  (SELECT 
    click_through_rate,
    conversion_rate,
    ad_text,
    time_of_day,
    day_of_week,
    audience_segment,
    keyword_match_type,
    bid_amount,
    ad_position,
    device_type,
    geographic_location,
    cost_per_click,
    impressions,
    clicks,
    conversions,
    revenue  -- Target variable
   FROM google_ads_performance
   WHERE revenue IS NOT NULL)
PREDICT revenue
USING 
  engine = 'lightwood',
  tag = 'google ads revenue optimization',
  time_column = 'timestamp',
  order_by = 'timestamp',
  group_by = 'campaign_id';