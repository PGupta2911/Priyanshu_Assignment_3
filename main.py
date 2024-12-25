import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

# Step 1: Configure user agent and headers
ua = UserAgent()  # Random User-Agent generator
headers = {
    'User-Agent': ua.random
}

# Step 2: Function to crawl LinkedIn public profiles
def crawl_linkedin(url):
    try:
        print(f"Fetching data from: {url}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Step 3: Extract profile or company details
            profile_name = soup.find('h1', {'class': 'text-heading-xlarge'}).text.strip() if soup.find('h1', {'class': 'text-heading-xlarge'}) else 'N/A'
            job_title = soup.find('div', {'class': 'text-body-medium'}).text.strip() if soup.find('div', {'class': 'text-body-medium'}) else 'N/A'
            location = soup.find('span', {'class': 'text-body-small'}).text.strip() if soup.find('span', {'class': 'text-body-small'}) else 'N/A'
            about_section = soup.find('section', {'class': 'pv-about-section'}).text.strip() if soup.find('section', {'class': 'pv-about-section'}) else 'N/A'

            # Return extracted data
            return {
                'Name': profile_name,
                'Job Title': job_title,
                'Location': location,
                'About': about_section
            }
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Step 4: Add pagination handling
def crawl_multiple_pages(base_url, num_pages=1):
    all_profiles = []
    for page in range(1, num_pages + 1):
        paginated_url = f"{base_url}?page={page}"  # Adjust URL structure as needed
        profile_data = crawl_linkedin(paginated_url)
        if profile_data:
            all_profiles.append(profile_data)
        time.sleep(2)  # Delay between requests to avoid getting blocked
    return all_profiles

# Example Usage:
if __name__ == "__main__":
    base_url = "https://www.linkedin.com/public-profile-url-example"  # Replace with an actual LinkedIn public profile URL
    profiles = crawl_multiple_pages(base_url, num_pages=3)  # Adjust number of pages as needed

    # Print the extracted profiles
    for i, profile in enumerate(profiles, start=1):
        print(f"\nProfile {i}:")
        for key, value in profile.items():
            print(f"{key}: {value}")
