#!/usr/bin/env python3
"""Test script for GitHub Trending Web API.

This script tests the web application's API endpoints without requiring a browser.
"""

import requests
import json
import time
from datetime import datetime


BASE_URL = "http://localhost:5000"


def test_health_check():
    """Test health check endpoint."""
    print("🏥 Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure the web app is running: python web_app.py")
        return False


def test_fetch_trending(period="weekly", language="", limit=10):
    """Test fetch trending endpoint.
    
    Args:
        period: daily, weekly, or monthly
        language: programming language (empty for all)
        limit: number of projects to fetch
    """
    print(f"\n🔍 Testing fetch endpoint...")
    print(f"   Period: {period}")
    print(f"   Language: {language or 'All Languages'}")
    print(f"   Limit: {limit}")
    
    try:
        payload = {
            "period": period,
            "language": language,
            "limit": limit,
            "enrich": False,  # Set to True if you have a GitHub token
            "github_token": ""  # Add your token here if needed
        }
        
        print(f"\n⏳ Fetching data (this may take a few seconds)...")
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/api/fetch",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['data']
                print(f"\n✅ Fetch successful! (took {elapsed:.1f}s)")
                print(f"\n📊 Results:")
                print(f"   - Projects fetched: {result['count']}")
                print(f"   - Period: {result['period']}")
                print(f"   - Language: {result['language']}")
                print(f"   - CSV file: {result['csv_file']}")
                print(f"   - Report file: {result['report_file']}")
                
                print(f"\n🏆 Top 5 Projects:")
                for i, project in enumerate(result['projects'][:5], 1):
                    print(f"\n   {i}. {project['repository_name']}")
                    print(f"      ⭐ Stars: {project['stars_total']:,}")
                    print(f"      📈 Period growth: +{project['stars_period']:,}")
                    if project.get('language'):
                        print(f"      💻 Language: {project['language']}")
                    if project.get('description'):
                        desc = project['description'][:80]
                        print(f"      📝 {desc}...")
                
                return True
            else:
                print(f"❌ Fetch failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - the server took too long to respond")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main test function."""
    print("=" * 60)
    print("🚀 GitHub Trending Web API Test")
    print("=" * 60)
    print()
    
    # Test 1: Health check
    if not test_health_check():
        print("\n⚠️  Web application is not running!")
        print("Please start it first:")
        print("  python web_app.py")
        return
    
    # Test 2: Fetch weekly trending Python projects
    print("\n" + "=" * 60)
    test_fetch_trending(period="weekly", language="python", limit=10)
    
    # Test 3: Fetch daily trending all languages
    print("\n" + "=" * 60)
    test_fetch_trending(period="daily", language="", limit=5)
    
    print("\n" + "=" * 60)
    print("✅ Tests completed!")
    print("=" * 60)
    print()
    print("💡 Visit http://localhost:5000 in your browser for the full experience")
    print()


if __name__ == '__main__':
    main()
