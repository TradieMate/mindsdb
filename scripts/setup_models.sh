#!/bin/bash

# Setup Analytics Optimization Models
# This script creates all the models needed for Google Ads and Website optimization

echo "Setting up MindsDB Analytics Optimization Models..."

# Wait for MindsDB to be ready
echo "Waiting for MindsDB to start..."
until curl -f http://localhost:47334/api/util/ping > /dev/null 2>&1; do
    echo "MindsDB not ready yet, waiting..."
    sleep 5
done

echo "MindsDB is ready! Creating models..."

# Directory containing model SQL files
MODEL_DIR="/mindsdb/sql/model_configurations"

# Execute each model configuration file in order
for sql_file in $(ls $MODEL_DIR/*.sql | sort); do
    echo "Executing: $(basename $sql_file)"
    
    # Use MindsDB HTTP API to execute SQL
    curl -X POST \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$(cat $sql_file | tr '\n' ' ' | sed 's/"/\\"/g')\"}" \
        http://localhost:47334/api/sql/query
    
    echo ""
    echo "Completed: $(basename $sql_file)"
    sleep 2
done

echo "All analytics optimization models have been created successfully!"
echo ""
echo "Available models:"
echo "- google_ads_optimizer: Revenue optimization for Google Ads"
echo "- website_conversion_optimizer: Website conversion rate optimization"
echo "- customer_journey_optimizer: Customer lifetime value prediction"
echo "- ad_text_performance: Ad text click-through rate optimization"
echo "- ads_forecaster: Revenue forecasting (time-series)"
echo "- ab_test_optimizer: A/B test performance prediction"
echo ""
echo "Check /mindsdb/sql/queries/ for example usage queries."