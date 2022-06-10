import csv
import webbrowser

from os.path import exists
from getpass import getpass
from datetime import date
from praw import Reddit
from prawcore import OAuthException
from colorama import Fore, Back

print("====================================================")
print("||                                                ||")
print("||           Reddit Digest Script v0.1.0          ||")
print("||                                                ||")
print("====================================================")

# Credential input loop
logged_in = False
reddit = None

while logged_in is False:
    username = input("Username: ")
    password = getpass()
    instance = Reddit(
        "user",
        username=username,
        password=password,
        user_agent="Reddit Digest Script"
    )

    print("Logging in...")
    try:
        redditor = instance.user.me()
        print(f"Logged in as {redditor}")
        logged_in = True
        reddit = instance
    except OAuthException:
        print("Error! Wrong credentials")

# Population loop
watchlist: list[tuple[str, str, int, str]] = []
tdysDate = date.today()

if exists(tdysDate.strftime("%m%d%Y") + ".csv"):
    print("A copy of today's digest was found! Loading...")
    with open(tdysDate.strftime("%m%d%Y") + ".csv") as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            watchlist.append((line[0], line[1], int(line[2]), line[3]))

else:
    with open(tdysDate.strftime("%m%d%Y") + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        for subreddit in reddit.user.subreddits(limit=None):
            if len(watchlist) == 1:
                print("Fetching subreddits...")

            iterator = subreddit.top(time_filter="day", limit=1)
            for submission in iterator:
                watchlist.append((subreddit.display_name, submission.title, submission.score, submission.shortlink))
                writer.writerow((subreddit.display_name, submission.title, submission.score, submission.shortlink))


def get_score(sub: tuple[str, str, int, str]):
    return sub[2]

# Sorting results
sortedlist = sorted(watchlist, key=get_score, reverse=True)
if len(sortedlist) > 15:
    sortedlist = sortedlist[:15]

# Display loop
while True:
    if len(sortedlist) == 0:  # Exit condition: no more remaining
        print("No more posts remaining! Try again tomorrow.")
        exit(0)

    # Display digest index
    print(f"====================================================")
    print(f"||                 Today's Digest                 ||")
    print(f"||                   {tdysDate}                   ||")
    print(f"====================================================")

    for idx, pair in enumerate(sortedlist):
        print(Fore.RESET + Back.RESET, f"{idx + 1}".ljust(3),
              Fore.GREEN + Back.RESET, f"[r/{pair[0]}]",
              Fore.CYAN + Back.RESET, pair[1],
              Fore.BLACK + Back.GREEN, pair[2],
              Fore.RESET + Back.RESET)

    print(Fore.BLUE + Back.RESET, "Enter number to view post details, or q to exit.",
          Fore.RESET + Back.RESET)

    # Input loop
    cmd = input("")
    if cmd == "q":  # Exit condition: input q
        exit(0)

    val = -1
    try:
        val = int(cmd)
    except ValueError:
        print("That's not a valid number!")

    if val < 1 or val > len(sortedlist):
        print("That post does not exist!")
    else:
        print("Opening!")
        webbrowser.open(sortedlist[val - 1][3])
        sortedlist.pop(val - 1)
