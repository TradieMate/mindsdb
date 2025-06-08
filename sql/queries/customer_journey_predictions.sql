-- Customer Journey Value Prediction Queries

-- 1. Predict customer lifetime value for high-engagement users
SELECT 
  predicted_customer_lifetime_value,
  confidence,
  first_touch_channel,
  last_touch_channel,
  touchpoint_count,
  journey_duration
FROM mindsdb.customer_journey_optimizer
WHERE 
  email_opens > 5
  AND website_visits > 3
  AND ad_interactions > 2
  AND content_downloads >= 1;

-- 2. Optimize first-touch channel strategies
SELECT 
  predicted_customer_lifetime_value,
  confidence,
  first_touch_channel,
  touchpoint_count
FROM mindsdb.customer_journey_optimizer
WHERE 
  email_clicks > 3
  AND social_media_interactions > 1
  AND demo_requests = 1
ORDER BY predicted_customer_lifetime_value DESC;

-- 3. Analyze journey duration impact
SELECT 
  predicted_customer_lifetime_value,
  confidence,
  journey_duration,
  touchpoint_count,
  last_touch_channel
FROM mindsdb.customer_journey_optimizer
WHERE 
  first_touch_channel = 'google_ads'
  AND website_visits >= 5
  AND email_opens > 2;

-- 4. Multi-channel attribution analysis
SELECT 
  predicted_customer_lifetime_value,
  confidence,
  first_touch_channel,
  last_touch_channel,
  social_media_interactions,
  email_clicks
FROM mindsdb.customer_journey_optimizer
WHERE 
  touchpoint_count >= 8
  AND journey_duration > 14
  AND content_downloads > 0
ORDER BY predicted_customer_lifetime_value DESC
LIMIT 15;