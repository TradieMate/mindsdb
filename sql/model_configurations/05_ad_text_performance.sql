-- Ad Text Click-Through Rate Optimization Model
-- Predicts CTR based on ad text characteristics

CREATE MODEL mindsdb.ad_text_performance
FROM supabase_analytics
  (SELECT 
    ad_headline,
    ad_description,
    call_to_action,
    ad_length,
    sentiment_score,
    keyword_density,
    emotional_triggers,
    urgency_words,
    benefit_mentions,
    click_through_rate  -- Target variable
   FROM ad_text_performance
   WHERE click_through_rate IS NOT NULL)
PREDICT click_through_rate
USING 
  engine = 'lightwood',
  tag = 'ad text ctr optimization';