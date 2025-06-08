#!/usr/bin/env python3
"""
Setup Analytics Optimization Models for MindsDB
This script creates all the models needed for Google Ads and Website optimization
"""

import os
import time
import requests
import json
from pathlib import Path

def wait_for_mindsdb(host="localhost", port=47334, timeout=300):
    """Wait for MindsDB to be ready"""
    url = f"http://{host}:{port}/api/util/ping"
    start_time = time.time()
    
    print("Waiting for MindsDB to start...")
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("MindsDB is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print("MindsDB not ready yet, waiting...")
        time.sleep(5)
    
    raise TimeoutError(f"MindsDB did not start within {timeout} seconds")

def execute_sql(query, host="localhost", port=47334):
    """Execute SQL query via MindsDB HTTP API"""
    url = f"http://{host}:{port}/api/sql/query"
    
    payload = {"query": query}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error executing query: {e}")
        return None

def setup_models():
    """Setup all analytics optimization models"""
    
    # Wait for MindsDB to be ready
    wait_for_mindsdb()
    
    # Path to model configuration files
    model_dir = Path("/mindsdb/sql/model_configurations")
    if not model_dir.exists():
        model_dir = Path("sql/model_configurations")
    
    if not model_dir.exists():
        print("Error: Model configuration directory not found!")
        return False
    
    # Get all SQL files and sort them
    sql_files = sorted(model_dir.glob("*.sql"))
    
    print(f"Found {len(sql_files)} model configuration files")
    print("Creating models...")
    
    success_count = 0
    for sql_file in sql_files:
        print(f"\nExecuting: {sql_file.name}")
        
        try:
            # Read SQL file
            with open(sql_file, 'r') as f:
                query = f.read()
            
            # Skip empty files or comments-only files
            if not query.strip() or query.strip().startswith('--'):
                print(f"Skipping {sql_file.name} (empty or comments only)")
                continue
            
            # Execute the query
            result = execute_sql(query)
            
            if result:
                print(f"✓ Completed: {sql_file.name}")
                success_count += 1
            else:
                print(f"✗ Failed: {sql_file.name}")
            
            # Small delay between model creations
            time.sleep(2)
            
        except Exception as e:
            print(f"✗ Error processing {sql_file.name}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Model setup completed!")
    print(f"Successfully created: {success_count}/{len(sql_files)} models")
    print(f"{'='*50}")
    
    if success_count > 0:
        print("\nAvailable models:")
        print("- google_ads_optimizer: Revenue optimization for Google Ads")
        print("- website_conversion_optimizer: Website conversion rate optimization") 
        print("- customer_journey_optimizer: Customer lifetime value prediction")
        print("- ad_text_performance: Ad text click-through rate optimization")
        print("- ads_forecaster: Revenue forecasting (time-series)")
        print("- ab_test_optimizer: A/B test performance prediction")
        print("\nCheck /mindsdb/sql/queries/ for example usage queries.")
    
    return success_count == len(sql_files)

if __name__ == "__main__":
    try:
        setup_models()
    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
    except Exception as e:
        print(f"Setup failed: {e}")
        exit(1)