from apify_client import ApifyClient
import os
import time
from dotenv import load_dotenv

load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Fetch LinkedIn jobs based on search query and location
def fetch_linkedin_jobs(search_query, location="Sri Lanka", rows=5):
    try:
        print(f"🔍 Searching LinkedIn jobs for: '{search_query}' in '{location}' (rows: {rows})")
        
        run_input = {
            "title": search_query,
            "location": location,
            "rows": rows,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"],
            }
        }
        
        print("📤 Starting LinkedIn job scraper...")
        run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
        
        # Wait for the run to complete
        print("⏳ Waiting for scraper to complete...")
        while run["status"] not in ["SUCCEEDED", "FAILED", "ABORTED"]:
            time.sleep(2)
            run = apify_client.run(run["id"]).get()
        
        print(f"✅ Scraper completed with status: {run['status']}")
        
        if run["status"] != "SUCCEEDED":
            print(f"❌ LinkedIn scraper failed with status: {run['status']}")
            return []
        
        # Get the dataset
        dataset_id = run["defaultDatasetId"]
        print(f"📊 Fetching data from dataset: {dataset_id}")
        
        jobs = list(apify_client.dataset(dataset_id).iterate_items())
        print(f"📋 Found {len(jobs)} LinkedIn jobs")
        
        # Debug: Print first job structure if available
        if jobs:
            print("🔍 Sample job structure:")
            first_job = jobs[0]
            for key, value in first_job.items():
                print(f"  {key}: {str(value)[:100]}...")
        
        return jobs
        
    except Exception as e:
        print(f"❌ Error fetching LinkedIn jobs: {str(e)}")
        return []

# Fetch Naukri jobs based on search query and location
def fetch_naukri_jobs(search_query, location="Sri Lanka", rows=5):
    try:
        print(f"🔍 Searching Naukri jobs for: '{search_query}' (maxJobs: 60)")
        
        run_input = {
            "keyword": search_query,
            "maxJobs": 60,  # Note: This is higher than the 'rows' parameter
            "freshness": "all",
            "sortBy": "relevance",
            "experience": "all",
        }
        
        print("📤 Starting Naukri job scraper...")
        run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
        
        # Wait for the run to complete
        print("⏳ Waiting for scraper to complete...")
        while run["status"] not in ["SUCCEEDED", "FAILED", "ABORTED"]:
            time.sleep(2)
            run = apify_client.run(run["id"]).get()
        
        print(f"✅ Scraper completed with status: {run['status']}")
        
        if run["status"] != "SUCCEEDED":
            print(f"❌ Naukri scraper failed with status: {run['status']}")
            return []
        
        # Get the dataset
        dataset_id = run["defaultDatasetId"]
        print(f"📊 Fetching data from dataset: {dataset_id}")
        
        jobs = list(apify_client.dataset(dataset_id).iterate_items())
        print(f"📋 Found {len(jobs)} Naukri jobs")
        
        # Limit to requested rows
        jobs = jobs[:rows] if len(jobs) > rows else jobs
        
        # Debug: Print first job structure if available
        if jobs:
            print("🔍 Sample job structure:")
            first_job = jobs[0]
            for key, value in first_job.items():
                print(f"  {key}: {str(value)[:100]}...")
        
        return jobs
        
    except Exception as e:
        print(f"❌ Error fetching Naukri jobs: {str(e)}")
        return []

# Alternative LinkedIn function with different parameters
def fetch_linkedin_jobs_alternative(search_query, location="Sri Lanka", rows=5):
    try:
        print(f"🔍 Alternative LinkedIn search for: '{search_query}' in '{location}'")
        
        # Try with different parameter structure
        run_input = {
            "keywords": search_query,  # Try 'keywords' instead of 'title'
            "location": location,
            "count": rows,  # Try 'count' instead of 'rows'
            "timeFilter": "anyTime",
            "sortBy": "mostRelevant"
        }
        
        print("📤 Starting alternative LinkedIn job scraper...")
        run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
        
        # Wait and process similar to above
        while run["status"] not in ["SUCCEEDED", "FAILED", "ABORTED"]:
            time.sleep(2)
            run = apify_client.run(run["id"]).get()
        
        if run["status"] != "SUCCEEDED":
            print(f"❌ Alternative LinkedIn scraper failed: {run['status']}")
            return []
        
        jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
        print(f"📋 Alternative method found {len(jobs)} LinkedIn jobs")
        
        return jobs
        
    except Exception as e:
        print(f"❌ Error with alternative LinkedIn fetch: {str(e)}")
        return []

# Function to test API and actor availability
def test_apify_connection():
    try:
        print("🧪 Testing Apify connection...")
        
        # Test if the API token is working
        user_info = apify_client.user().get()
        print(f"✅ Connected as: {user_info.get('username', 'Unknown user')}")
        
        # Test LinkedIn actor
        linkedin_actor = apify_client.user().get()
        print("✅ LinkedIn actor accessible")
        
        # Test Naukri actor  
        naukri_actor = apify_client.user().get()
        print("✅ Naukri actor accessible")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")
        return False

# Updated main functions with better error handling
def fetch_linkedin_jobs_improved(search_query, location="Sri Lanka", rows=5):
    """
    Improved LinkedIn job fetching with multiple fallback strategies
    """
    
    # First, try the original method
    jobs = fetch_linkedin_jobs(search_query, location, rows)
    
    # If no jobs found, try alternative method
    if not jobs:
        print("🔄 Trying alternative LinkedIn search method...")
        jobs = fetch_linkedin_jobs_alternative(search_query, location, rows)
    
    # If still no jobs, try with different location
    if not jobs and location != "worldwide":
        print("🔄 Trying worldwide search...")
        jobs = fetch_linkedin_jobs(search_query, "worldwide", rows)
    
    return jobs