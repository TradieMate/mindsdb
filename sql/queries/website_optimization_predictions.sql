-- Website Conversion Rate Optimization Queries

-- 1. Get conversion rate predictions for page improvements
SELECT 
  predicted_conversion_rate,
  confidence,
  page_load_time,
  traffic_source,
  device_type,
  bounce_rate
FROM mindsdb.website_conversion_optimizer
WHERE 
  bounce_rate < 0.3
  AND session_duration > 120
  AND pages_per_session > 2
  AND page_load_time < 3.0;

-- 2. Optimize page load times for different traffic sources
SELECT 
  predicted_conversion_rate,
  confidence,
  page_load_time,
  traffic_source
FROM mindsdb.website_conversion_optimizer
WHERE 
  bounce_rate = 0.25
  AND session_duration = 180
  AND device_type = 'mobile'
ORDER BY predicted_conversion_rate DESC;

-- 3. Test different device experiences
SELECT 
  predicted_conversion_rate,
  confidence,
  device_type,
  browser_type,
  scroll_depth
FROM mindsdb.website_conversion_optimizer
WHERE 
  page_load_time = 2.5
  AND traffic_source = 'google_ads'
  AND time_on_page > 60;

-- 4. Geographic optimization
SELECT 
  predicted_conversion_rate,
  confidence,
  geographic_location,
  traffic_source,
  device_type
FROM mindsdb.website_conversion_optimizer
WHERE 
  bounce_rate < 0.4
  AND pages_per_session >= 3
  AND button_clicks > 2
ORDER BY predicted_conversion_rate DESC
LIMIT 20;