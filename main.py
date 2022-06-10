import webbrowser
import getpass

from datetime import date
from praw import Reddit
from praw.models import Submission, Subreddit
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
    password = getpass.getpass()
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
watchlist = []

for subreddit in reddit.user.subreddits(limit=None):
    if len(watchlist) == 1:
        print("Fetching subreddits...")

    iterator = subreddit.top(time_filter="day", limit=1)
    for submission in iterator:
        submission: Submission
        watchlist.append((subreddit, submission))


def get_score(sub: tuple[Subreddit, Submission]):
    return sub[1].score


# Sorting results
sortedlist = sorted(watchlist, key=get_score, reverse=True)
if len(sortedlist) > 15:
    sortedlist = sortedlist[:15]

# Display loop
while True:
    # Display digest index
    tdysDate = date.today()
    print(f"====================================================")
    print(f"||                 Today's Digest                 ||")
    print(f"||                   {tdysDate}                   ||")
    print(f"====================================================")

    for idx, pair in enumerate(sortedlist):
        print(Fore.RESET + Back.RESET, f"{idx + 1}".ljust(3),
              Fore.GREEN + Back.RESET, f"[r/{pair[0].display_name}]",
              Fore.CYAN + Back.RESET, pair[1].title,
              Fore.BLACK + Back.GREEN, pair[1].score,
              Fore.RESET + Back.RESET)

    print(Fore.BLUE + Back.RESET, "Enter number to view post details, or q to exit.",
          Fore.RESET + Back.RESET)

    # Input loop
    cmd = input("")
    if cmd == "q":  # Exit condition: input q
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
        sortedlist.pop(val - 1)

        if len(sortedlist) == 0:  # Exit condition: no more remaining
            print("No more remaining! Come again tomorrow.")
            exit(1)
