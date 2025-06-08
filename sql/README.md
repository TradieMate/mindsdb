# MindsDB Analytics Optimization Models

This directory contains pre-configured machine learning models for Google Ads and website analytics optimization.

## 🎯 Models Included

### 1. **Google Ads Revenue Optimizer** (`google_ads_optimizer`)
- **Purpose**: Predicts revenue based on ad performance metrics
- **Input**: CTR, conversion rate, ad text, timing, audience, bid amount, etc.
- **Output**: Predicted revenue with confidence scores

### 2. **Website Conversion Optimizer** (`website_conversion_optimizer`)  
- **Purpose**: Predicts conversion rates for website optimization
- **Input**: Page load time, bounce rate, traffic source, device type, etc.
- **Output**: Predicted conversion rate with confidence scores

### 3. **Customer Journey Optimizer** (`customer_journey_optimizer`)
- **Purpose**: Predicts customer lifetime value from journey touchpoints
- **Input**: Touch channels, email interactions, website visits, etc.
- **Output**: Predicted customer lifetime value

### 4. **Ad Text Performance** (`ad_text_performance`)
- **Purpose**: Optimizes ad text for click-through rates
- **Input**: Headlines, descriptions, CTAs, sentiment, keywords, etc.
- **Output**: Predicted click-through rate

### 5. **Ads Revenue Forecaster** (`ads_forecaster`)
- **Purpose**: Time-series forecasting for ad revenue (7-day predictions)
- **Input**: Historical daily performance data
- **Output**: Future revenue predictions

### 6. **A/B Test Optimizer** (`ab_test_optimizer`)
- **Purpose**: Predicts performance of A/B test variants
- **Input**: Test variants, user segments, page versions, etc.
- **Output**: Predicted conversion rates for variants

## 🚀 Quick Setup

### Automatic Setup (Recommended)
```bash
# Run the setup script after MindsDB starts
python3 scripts/setup_models.py
```

### Manual Setup
```bash
# Execute each model file individually
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "$(cat sql/model_configurations/01_supabase_connection.sql)"}' \
  http://localhost:47334/api/sql/query
```

## 🔧 Configuration

### Environment Variables
Set these before running the setup:

```bash
export SUPABASE_USER="your_supabase_user"
export SUPABASE_PASSWORD="your_supabase_password"  
export SUPABASE_HOST="your_project.supabase.co"
```

### Required Supabase Tables
Your Supabase database should have these tables:

- `google_ads_performance` - Google Ads metrics
- `website_analytics` - Website performance data
- `customer_journey_data` - Customer touchpoint data
- `ad_text_performance` - Ad creative performance
- `daily_ad_performance` - Time-series ad data
- `ab_test_results` - A/B test results

## 📊 Usage Examples

### Get Google Ads Recommendations
```sql
SELECT predicted_revenue, confidence, ad_text, bid_amount
FROM mindsdb.google_ads_optimizer
WHERE click_through_rate = 0.05 
  AND audience_segment = 'high-intent'
  AND device_type = 'mobile';
```

### Optimize Website Conversion
```sql
SELECT predicted_conversion_rate, confidence, page_load_time
FROM mindsdb.website_conversion_optimizer  
WHERE bounce_rate < 0.3
  AND session_duration > 120;
```

### Forecast Ad Revenue
```sql
SELECT predicted_daily_revenue, date, campaign_id
FROM mindsdb.ads_forecaster
WHERE campaign_id = 'campaign_123' 
  AND date > LATEST;
```

## 📁 Directory Structure

```
sql/
├── model_configurations/     # Model creation SQL files
│   ├── 01_supabase_connection.sql
│   ├── 02_google_ads_optimizer.sql
│   ├── 03_website_conversion_optimizer.sql
│   ├── 04_customer_journey_optimizer.sql
│   ├── 05_ad_text_performance.sql
│   ├── 06_ads_forecaster.sql
│   └── 07_ab_test_optimizer.sql
├── queries/                  # Example query files
│   ├── google_ads_predictions.sql
│   ├── website_optimization_predictions.sql
│   ├── customer_journey_predictions.sql
│   └── README.md
└── README.md                # This file
```

## 🐳 Docker Integration

These models are automatically available when you build the Docker image. The setup scripts are included in the container and can be run after MindsDB starts.

### In docker-compose.yml:
```yaml
mindsdb:
  environment:
    SUPABASE_USER: "${SUPABASE_USER}"
    SUPABASE_PASSWORD: "${SUPABASE_PASSWORD}"
    SUPABASE_HOST: "${SUPABASE_HOST}"
  volumes:
    - ./sql:/mindsdb/sql
    - ./scripts:/mindsdb/scripts
```

## 🔍 Monitoring

Check model status:
```sql
SELECT name, status, training_time 
FROM mindsdb.models 
WHERE name LIKE '%optimizer%' OR name LIKE '%forecaster%';
```

## 🛠️ Troubleshooting

1. **Connection Issues**: Verify Supabase credentials and network connectivity
2. **Missing Tables**: Ensure your Supabase database has the required table structure
3. **Model Training Fails**: Check data quality and ensure target columns have non-null values
4. **Low Confidence**: May need more training data or feature engineering

## 📈 Expected Performance

- **Training Time**: 2-10 minutes per model (depending on data size)
- **Prediction Speed**: < 100ms per query
- **Accuracy**: Typically 80-95% depending on data quality and use case
- **Confidence Scores**: Available for all predictions to assess reliability