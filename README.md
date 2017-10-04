# SlackBot-OracleServiceCloud
A slack bot to access and close Oracle Service Cloud 311s (incidents)

The base bot code was taken from [How to Build Your First Slack Bot With Python](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)

The functions are my python code to access Oracle Service Cloud.

This code needs a LOT of refactoring. This is a first pass to make it work. Almost all REST API calls are the same so should be rolledi n to a single function. All the If() statements for each function should be changed/simplified. Maybe each call - show, case, help, close, 311 - should be put in a seperate file or files. Single python function for each type of call/request?
