-- Google Ads Revenue Optimization Queries

-- 1. Get revenue predictions for new ad configurations
SELECT 
  predicted_revenue,
  confidence,
  ad_text,
  time_of_day,
  bid_amount,
  device_type
FROM mindsdb.google_ads_optimizer
WHERE 
  click_through_rate = 0.05
  AND audience_segment = 'high-intent'
  AND device_type = 'mobile'
  AND time_of_day = '18:00';

-- 2. Find optimal bid amounts for different audience segments
SELECT 
  predicted_revenue,
  confidence,
  bid_amount,
  audience_segment
FROM mindsdb.google_ads_optimizer
WHERE 
  click_through_rate = 0.03
  AND ad_position <= 3
  AND device_type = 'desktop'
ORDER BY predicted_revenue DESC
LIMIT 10;

-- 3. Test different ad texts for performance
SELECT 
  predicted_revenue,
  confidence,
  ad_text,
  predicted_click_through_rate
FROM mindsdb.google_ads_optimizer
WHERE 
  audience_segment = 'lookalike'
  AND bid_amount = 2.50
  AND device_type = 'mobile';

-- 4. Optimize for different times of day
SELECT 
  predicted_revenue,
  confidence,
  time_of_day,
  day_of_week
FROM mindsdb.google_ads_optimizer
WHERE 
  click_through_rate = 0.04
  AND audience_segment = 'retargeting'
  AND device_type = 'tablet'
ORDER BY predicted_revenue DESC;