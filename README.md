# reddit-account-generator

reddit-account-generator is a simple script written in python3 that helps you to create reddit accounts automatically. It uses selenium_stealth so it undetectable. For the username name creation it directly requests reddit for suggested usernames and selects them. If reddit servers deny the request then it will randomly create a username. It also verifies the email and saves the account info in a text file.

## Usuage
```
pip install -r requirements.txt
python main.py
```

## Screenshot

![screenshot](https://github.com/anuj66283/reddit-account-generator/blob/master/screenshot.PNG)

# Note
This script is not threaded.
