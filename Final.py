import praw
import requests
import schedule
import time
import logging
from datetime import datetime
import random

# Set up logging with more detailed formatting
logging.basicConfig(
    filename='reddit_bot_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class RedditBot:
    def __init__(self):
        # Initialize Reddit API connection
        self.reddit = praw.Reddit(
            client_id='IXGB6Zzka6ig1eqDXzKZZg',
            client_secret='oPGRKWPCGXcpT5yC94lPKid9rAnTsg',
            username='Current-Minimum3188',
            password='AimHigh#1',
            user_agent='sowmi'
        )
        
        # Groq API configuration
        self.groq_api_key = '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'
        self.groq_url = 'https://api.groq.com/openai/v1/chat/completions'
        
        # Bot configuration
        self.target_subreddit = 'test'  # Change this to your target subreddit
        self.post_times = ['10:00', '15:13', '18:00', '19:00','20:00']  # Multiple posting times
        
        # List of prompts for variety
        self.prompts = [
            "Write an interesting fact about space in two sentences.",
            "Share a fascinating historical event from this day in history.",
            "Explain a mind-blowing scientific concept in simple terms.",
            "Tell an interesting fact about the human body.",
            "Share a surprising fact about technology or AI."
        ]

    def generate_content(self, prompt):
        """Generate content using Groq AI"""
        data = {
            "model": "mixtral-8x7b-32768",
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "temperature": 0.7,
            "max_tokens": 150
        }
        
        headers = {"Authorization": f"Bearer {self.groq_api_key}"}
        
        try:
            response = requests.post(self.groq_url, json=data, headers=headers)
            response.raise_for_status()
            
            content = response.json().get('choices', [{}])[0].get('message', {}).get('content', None)
            if content:
                logging.info("Successfully generated content")
                return content
            else:
                logging.error(f"Groq API response error: {response.json()}")
                return None
                
        except Exception as e:
            logging.error(f"Error generating content: {str(e)}")
            return None

    def post_to_reddit(self, title, content):
        """Post content to Reddit"""
        try:
            subreddit = self.reddit.subreddit(self.target_subreddit)
            submission = subreddit.submit(title, selftext=content)
            post_url = f"https://reddit.com{submission.permalink}"
            
            logging.info(f"Successfully posted to r/{self.target_subreddit}. URL: {post_url}")
            print(f"Posted successfully: {post_url}")
            
            return True
            
        except Exception as e:
            logging.error(f"Error posting to Reddit: {str(e)}")
            print(f"Error posting to Reddit: {str(e)}")
            return False

    def create_post(self):
        """Create and submit a post"""
        try:
            # Select random prompt
            prompt = random.choice(self.prompts)
            
            # Generate content
            content = self.generate_content(prompt)
            
            if content:
                # Create title based on current time
                current_time = datetime.now().strftime("%Y-%m-%d")
                title = f"Daily Interesting Fact - {current_time}"
                
                # Post to Reddit
                self.post_to_reddit(title, content)
            else:
                logging.error("Failed to generate content")
                
        except Exception as e:
            logging.error(f"Error in create_post: {str(e)}")

    def schedule_posts(self):
        """Schedule posts for specified times"""
        for post_time in self.post_times:
            schedule.every().day.at(post_time).do(self.create_post)
            logging.info(f"Scheduled post for {post_time}")

    def run(self):
        """Main bot loop"""
        print(f"Bot starting up... Authenticated as: {self.reddit.user.me()}")
        logging.info("Bot started")
        
        # Schedule posts
        self.schedule_posts()
        
        # Run continuously
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check schedule every minute
            except Exception as e:
                logging.error(f"Error in main loop: {str(e)}")
                time.sleep(300)  # Wait 5 minutes if there's an error

if __name__ == "__main__":
    # Create and run the bot
    bot = RedditBot()
    bot.run()