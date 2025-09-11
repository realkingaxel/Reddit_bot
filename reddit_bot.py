import requests
import praw
import random
import sys, os
import schedule
import time
from datetime import datetime, timedelta
import pyfiglet
from colorama import Fore, Back, Style, init

used_subreddits = []


def get_input_int_post(text):
    while True:
        try:
            user_input = int(input(f"{text}: {Fore.YELLOW}"))
            return user_input
        except ValueError as e:
            print(f"{Fore.RED}please input a number...")
        

def get_input_int(text, text2):
    while True:
        try:
            user_input = int(input(f"{text}: {Fore.YELLOW}"))
            if 0 > user_input or user_input > 23:
                print(f"{Fore.RED}{text2} hour has to be between 0 and 23...")
            else:
                return user_input

            
        except ValueError as e:
            print(f"{Fore.RED}please input a number...")
        

def resource_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    return os.path.join(os.path.dirname(__file__), filename)


def show_reddit_bot_banner():
    banner = pyfiglet.figlet_format("Redible  Bot", font="standard")
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.GREEN + "-" * 50)
    print("Reddit bot online. Listening for karma...")
    print("-" * 50 + Style.RESET_ALL)

def schedule_random_times(start_time, end_time, posts_per_day):
    schedule.clear()
    scheduled_times = set()

    while len(scheduled_times) < posts_per_day:
        rand_hour = random.randint(start_time,end_time)
        rand_minute = random.randint(0,59)
        time_str = f"{rand_hour:02d}:{rand_minute:02d}"
        if time_str not in scheduled_times:
            scheduled_times.add(time_str)
            schedule.every().day.at(time_str).do(post_reddit)
            print(f"{Fore.LIGHTMAGENTA_EX}scheduled post at {time_str}")


def post_reddit():
    images = [f for f in os.listdir(resource_path("images")) if f.lower().endswith((".jpg", 'png', "jpeg", "gif", ".heic"))]
    selected_image = random.choice(images)
    selected_image = os.path.join("images", selected_image)
    with open(resource_path("titles.txt"), "r", encoding='utf-8') as f:
        titles = [line.strip() for line in f]
    with open(resource_path("subreddits.txt"), "r") as g:
        subreddits = [line.strip() for line in g]
    selected_title = random.choice(titles)
    selected_subreddit = random.choice(subreddits)
    while True:
        if len(subreddits) == len(used_subreddits):
            return(print("Post failed: all subreddits used today"))
        if selected_subreddit in used_subreddits:
            selected_subreddit = random.choice(subreddits)
            continue
        else:
            used_subreddits.append(selected_subreddit)
            break
    subreddit = reddit.subreddit(f"{selected_subreddit}")
    try:
        subreddit.submit_image(title=selected_title, image_path = selected_image)
    except Exception as e:
        print(f"Post failed: {e}")


def load_credentials(file_path):
     creds={}
     with open(file_path, "r") as f:
          for line in f:
               key, value = line.strip().split("=",1)
               creds[key] = value
     return creds

init()
show_reddit_bot_banner()

while True:
    key = str(input(f"{Fore.BLUE}Enter your license key: {Fore.YELLOW}"))
    license_key  = {'license-key': f"{key}"}
    response = requests.post("https://license-server-oo4e.onrender.com/check-license", json = license_key)
    if response.status_code == 200:
        response_server = response.json().get('message')
        if response_server == "success":
            print(f"{Fore.GREEN}Your key is valid!")
            break
        else:
            print(f"{Fore.RED}invalid key...Try again")
    else:
        print(f"Error: {response.json()}")
    
    
   


while True:
        credentials = load_credentials(resource_path('reddit_credentials.txt'))
        
        reddit = praw.Reddit(
        client_id= credentials["client_id"],
        client_secret= credentials["client_secret"],
        username=credentials["username"],
        password=credentials["password"],
        user_agent=f'python:myredditbot:v1.0 (by u/{credentials["username"]})'
        )
        
        try:
          user = reddit.user.me()
          if user:
             print("Connected successfully to Reddit API as:", user)
             break
        except Exception as e:
          print(f"{Fore.RED}Failed to connect to reddit API exiting app...")
          exit()

while True:
    start_time_post = get_input_int(f"{Fore.BLUE}Enter start hour for posts (0-23)", "Start")
    end_time_post = get_input_int(f"{Fore.BLUE}Enter end hour for posts (0-23)", "End")
    if start_time_post>end_time_post:
        print(f"{Fore.RED}Start hour cannot be before end time...")
    else:
        print(f"{Fore.LIGHTMAGENTA_EX}Posts will be scheduled randomly between {start_time_post}:00--{end_time_post}:59")
        break
while True:  
    number_posts = get_input_int_post(f"{Fore.BLUE}how many posts per day?")
    if number_posts < 10:
        break
    else:
        print(f"{Fore.RED}Don't post too much reddit will ban you...")

schedule_random_times(start_time_post, end_time_post, number_posts)
current_day = datetime.now().day
print(f"{Fore.GREEN}Bot is now running press CTRL-C to exit{Style.RESET_ALL}")
while True:
    
    schedule.run_pending()
    time.sleep(10)
    new_day = datetime.now().day

    if new_day != current_day:
        print("New day detected. Rescheduling posts...")
        used_subreddits = []
        current_day = new_day
        schedule_random_times(start_time_post, end_time_post, number_posts)
    
    

    



