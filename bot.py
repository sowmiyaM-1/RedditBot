import praw
import requests
import schedule
import time
import logging
from groq import Groq

# Set up logging to track bot's activities
logging.basicConfig(
    filename='bot_logg',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Initialize Reddit API connection
reddit = praw.Reddit(
    client_id='IXGB6Zzka6ig1eqDXzKZZg',
    client_secret='oPGRKWPCGXcpT5yC94lPKid9rAnTsg',
    username='Current-Minimum3188',
    password='AimHigh#1',
    user_agent='sowmi'
)





def generate_content(prompt):
    api_key = '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'
    url = 'https://api.groq.com/openai/v1/chat/completions'
    
    # Updated model name for Groq
    data = {
        "model": "mixtral-8x7b-32768",  # Groq's model
        "messages": [{
            "role": "user",
            "content": prompt
        }],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        # Add debug logging
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        
        response.raise_for_status()
        
        content = response.json().get('choices', [{}])[0].get('message', {}).get('content', None)
        if content:
            print("Generated content:", content)  # Debug print
            return content
        else:
            logging.error(f"Groq API response error: {response.json()}")
            return None
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Groq API Error: {str(e)}")
        print(f"Error details: {str(e)}")  # Debug print
        return None
    
    

def test_generation():
    test_prompt = "Write a single interesting fact about space in one sentence."
    print("Sending prompt:", test_prompt)
    result = generate_content(test_prompt)
    print("Result:", result)

# Run the test
test_generation()

def post_to_reddit(subreddit_name, title, content):
 
    try:
        subreddit = reddit.subreddit(subreddit_name)
        subreddit.submit(title, selftext=content)
        logging.info(f"Successfully posted to {subreddit_name}")
    except Exception as e:
        logging.error(f"Error posting to Reddit: {str(e)}")

def daily_task():
  
    prompt = "Write an interesting fact about space."
    content = generate_content(prompt)
    print(content)
    
    if content:
        post_to_reddit("YOUR_SUBREDDIT", "Daily Space Fact", content)

# Schedule the daily task
schedule.every().day.at("11:31").do(daily_task)

# Main loop to keep the bot running
def main():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()