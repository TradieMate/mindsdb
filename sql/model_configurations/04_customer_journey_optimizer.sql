-- Customer Journey Value Prediction Model
-- Predicts customer lifetime value based on journey touchpoints

CREATE MODEL mindsdb.customer_journey_optimizer
FROM supabase_analytics
  (SELECT 
    first_touch_channel,
    last_touch_channel,
    touchpoint_count,
    journey_duration,
    email_opens,
    email_clicks,
    social_media_interactions,
    website_visits,
    ad_interactions,
    content_downloads,
    demo_requests,
    customer_lifetime_value  -- Target variable
   FROM customer_journey_data
   WHERE customer_lifetime_value IS NOT NULL)
PREDICT customer_lifetime_value
USING 
  engine = 'lightwood',
  tag = 'customer journey value prediction',
  time_column = 'journey_start_date',
  order_by = 'journey_start_date';