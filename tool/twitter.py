import tweepy
from dotenv import load_dotenv
from crewai_tools import tool
import os

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')
# print(bearer_token)
@tool("Post a tweet on twitter")
def tweet(text):
    """Tool to make a tweet on twitter based on the text being passed. Example Usage: tweet("Hello World!)"""
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    response = client.create_tweet(text=text)
    print(f"https://twitter.com/user/status/{response.data['id']}")

