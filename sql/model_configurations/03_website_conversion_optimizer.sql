-- Website Conversion Rate Optimization Model
-- Predicts conversion rates based on website analytics

CREATE MODEL mindsdb.website_conversion_optimizer
FROM supabase_analytics
  (SELECT 
    page_load_time,
    bounce_rate,
    session_duration,
    pages_per_session,
    traffic_source,
    device_type,
    browser_type,
    geographic_location,
    time_on_page,
    scroll_depth,
    button_clicks,
    form_interactions,
    exit_rate,
    conversion_rate  -- Target variable
   FROM website_analytics
   WHERE conversion_rate IS NOT NULL)
PREDICT conversion_rate
USING 
  engine = 'lightwood',
  tag = 'website conversion optimization',
  time_column = 'date',
  order_by = 'date',
  group_by = 'page_url';