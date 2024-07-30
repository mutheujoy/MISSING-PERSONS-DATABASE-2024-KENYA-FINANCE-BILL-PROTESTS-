import tweepy
import os
from datetime import datetime

# Load environment variables
api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define search parameters
search_keywords = ["missing", "Kenya", "Nairobi"]
query = " OR ".join(search_keywords) + " -filter:retweets"
date_since = "2024-01-01"  # Adjust date as needed
max_tweets = 100

def fetch_tweets(query, date_since, max_tweets):
    """Fetch tweets containing the specified query."""
    tweets = tweepy.Cursor(api.search_tweets,
                           q=query,
                           lang="en",
                           since=date_since,
                           tweet_mode='extended').items(max_tweets)

    tweet_data = []
    for tweet in tweets:
        tweet_info = {
            'id': tweet.id_str,
            'text': tweet.full_text,
            'created_at': tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'user': tweet.user.screen_name,
            'user_location': tweet.user.location,
            'retweet_count': tweet.retweet_count,
            'favorite_count': tweet.favorite_count
        }
        tweet_data.append(tweet_info)

    return tweet_data

def save_tweets(tweets, filename="data/tweets_data.json"):
    """Save tweets to a JSON file."""
    import json
    with open(filename, 'w') as file:
        json.dump(tweets, file, indent=4)

# Fetch and save tweets
tweets = fetch_tweets(query, date_since, max_tweets)
save_tweets(tweets)

print(f"Fetched and saved {len(tweets)} tweets.")
