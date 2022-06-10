# Reddit Digest Script

Simple script to get a daily digest from Reddit, written in Python with the [PRAW](https://github.com/praw-dev/praw) library.

This script is really really simple! It fetches the top post every day from your followed subreddits, then chooses the top 15 in terms of score. Nothing more than that.

Mostly just to practise my rusty beginner Python skills.

### Usage
1. Create a personal use script in your [Reddit apps](https://www.reddit.com/prefs/apps).
2. Fill in the Client ID and Client secret blanks in the praw.ini.example file.
3. Rename praw.ini.example to praw.ini
4. Run main.py