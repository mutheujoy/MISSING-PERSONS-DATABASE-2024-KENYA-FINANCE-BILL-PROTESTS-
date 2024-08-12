import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Function to scrape data from X.com (formerly Twitter) using the Twitter API
def scrape_twitter(query, bearer_token):
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
    }
    params = {
        "query": query,
        "tweet.fields": "created_at,author_id,text",
        "start_time": "2024-07-01T00:00:00Z",
        "max_results": 100,
    }
    response = requests.get(url, headers=headers, params=params)
    tweets = response.json()
    return tweets

# Function to scrape data from Facebook using the Facebook Graph API
def scrape_facebook(query, access_token):
    url = f"https://graph.facebook.com/v10.0/search"
    params = {
        "q": query,
        "type": "post",
        "since": "2024-07-01",
        "access_token": access_token,
    }
    response = requests.get(url, params=params)
    posts = response.json()
    return posts

# Function to scrape data from Instagram using the Instagram Graph API
def scrape_instagram(hashtag, access_token):
    url = f"https://graph.instagram.com/v10.0/ig_hashtag_search"
    params = {
        "user_id": "self",
        "q": hashtag,
        "access_token": access_token,
    }
    response = requests.get(url, params=params)
    hashtags = response.json()
    return hashtags

# Function to scrape data from TikTok (using a web scraping approach as there is no public API)
def scrape_tiktok(query):
    url = f"https://www.tiktok.com/tag/{query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tiktoks = []
    for video in soup.find_all('div', {'class': 'tiktok-post'}):
        tiktoks.append({
            'username': video.find('a', {'class': 'tiktok-username'}).text,
            'description': video.find('div', {'class': 'tiktok-description'}).text,
            'date': video.find('span', {'class': 'tiktok-date'}).text,
        })
    return tiktoks

if __name__ == "__main__":
    twitter_bearer_token = "YOUR_TWITTER_BEARER_TOKEN"
    facebook_access_token = "YOUR_FACEBOOK_ACCESS_TOKEN"
    instagram_access_token = "YOUR_INSTAGRAM_ACCESS_TOKEN"
    query = "missing persons Kenya 2024"

    # Scrape data from Twitter
    twitter_data = scrape_twitter(query, twitter_bearer_token)
    print("Twitter Data:", json.dumps(twitter_data, indent=2))

    # Scrape data from Facebook
    facebook_data = scrape_facebook(query, facebook_access_token)
    print("Facebook Data:", json.dumps(facebook_data, indent=2))

    # Scrape data from Instagram
    instagram_data = scrape_instagram(query.replace(" ", ""), instagram_access_token)
    print("Instagram Data:", json.dumps(instagram_data, indent=2))

    # Scrape data from TikTok
    tiktok_data = scrape_tiktok(query.replace(" ", ""))
    print("TikTok Data:", json.dumps(tiktok_data, indent=2))
