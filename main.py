import webbrowser

import praw
import getpass

from praw.models import Submission, Subreddit
from prawcore import OAuthException
from colorama import Fore, Back

logged_in = False
reddit = None

while logged_in is False:
    username = input("Username: ")
    password = getpass.getpass()

    print("Logging in...")

    instance = praw.Reddit(
        "user",
        username=username,
        password=password,
        user_agent="Reddit Digest Script"
    )

    try:
        redditor = instance.user.me()
        print(f"Logged in as {redditor}")
        logged_in = True
        reddit = instance
    except OAuthException:
        print("Error! Wrong credentials")

watchlist = []
fetch_sub_count = 0

for subreddit in reddit.user.subreddits(limit=None):
    fetch_sub_count += 1
    print(f"Fetched {fetch_sub_count} subreddits")

    iterator = subreddit.top(time_filter="day", limit=1)
    for submission in iterator:
        submission: Submission
        watchlist.append((subreddit, submission))


def get_score(sub: tuple[Subreddit, Submission]):
    return sub[1].score


sortedlist = sorted(watchlist, key=get_score, reverse=True)
if len(sortedlist) > 15:
    sortedlist = sortedlist[:15]

while True:
    for idx, pair in enumerate(sortedlist):
        print(Fore.RESET + Back.RESET, idx + 1,
              Fore.GREEN + Back.RESET, f"[r/{pair[0].display_name}]",
              Fore.CYAN + Back.RESET, pair[1].title,
              Fore.BLACK + Back.GREEN, pair[1].score,
              Fore.RESET + Back.RESET)

    print(Fore.BLUE + Back.RESET, "Enter number to view post details, or q to exit.",
          Fore.RESET + Back.RESET)

    cmd = input("")
    if cmd == "q":
        exit(1)

    val = -1
    try:
        val = int(cmd)
    except ValueError:
        print("That's not a valid number!")

    if val < 1 or val > len(sortedlist):
        print("That post does not exist!")

    else:
        print("Opening!")
        webbrowser.open(sortedlist[val - 1][1].shortlink)