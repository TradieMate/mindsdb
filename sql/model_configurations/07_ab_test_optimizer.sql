-- A/B Test Performance Optimization Model
-- Predicts conversion rates for different test variants

CREATE MODEL mindsdb.ab_test_optimizer
FROM supabase_analytics
  (SELECT 
    test_variant,
    user_segment,
    page_version,
    traffic_source,
    device_type,
    test_duration,
    sample_size,
    conversion_rate,
    statistical_significance
   FROM ab_test_results
   WHERE conversion_rate IS NOT NULL)
PREDICT conversion_rate
USING 
  engine = 'lightwood',
  tag = 'ab test performance prediction';