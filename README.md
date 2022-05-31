# Covid19 Telegram Bot
A general purpose bot for accessing the latest information about Covid19 in India. Built for a college project

# ARCHIVED

[Covid19India](https://github.com/covid19india) stopped [its operations on October 31st, 2021](https://blog.covid19india.org/2021/08/07/end/)

While currently the API is still publicly accessible and can be used to fetch past data, that might change by the time you are reading this. I would like to thank everyone at Covid19India who spent these 16 months building and maintaining something of this quality. 

Since this project primarily relies on Covid19India's API to fetch the latest data, it only makes sense to archive it. 

You're still free to clone and use it. It should still work as expected, albeit with outdated data.

## Sources
 
1. [Covid19 India](https://github.com/covid19india/api)
2. [Pomber Covid19](https://github.com/pomber/covid19)
 
## How to use
 
 The Bot can be found under @MyTelegramCovidBot on Telegram. Say hello to it from us!

## Available commands 

Type `\help` to see the various available commands

## Note

While the use of these commands is recommended, its made clear that the bot can understand Natural Language with the help of specific keywords. For example, instead of `/graph daily India total UP MH` you can enter `daily new cases Maharashtra and Delhi`. 

The bot will try to autocorrect, so misspellings of countries and states should work. However, as expected, none of this is perfect. You're advised to be as specific as possible to get the best possible response. If even that fails, try using the `/helpmode`.

Try being as specific as possible to get the best response.

## Dependencies

1. [python-telegram-bot](https://python-telegram-bot.org/)
2. [matplotlib](https://matplotlib.org/)
3. [numpy](https://numpy.org/)
4. [pytz](https://pypi.org/project/pytz/)
5. [requests](https://requests.readthedocs.io/en/master/)

 ## How to contribute
 
 You can clone the project by entering the following in your terminal
 
 ```
 $ git clone https://github.com/TheTrio/Covid19-India-Telegram-Bot.git
 ```

You're expected to have an API Token for your Telegram chat bot, and that is to be saved in a file named `token`, located in the same directory as the rest of these files. If you're not sure what that means, please read [this](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) quick and easy tutorial.

You must also make a variable named `chat_id` with the chat_id of the user you wish to send regular updates to. Presently, this bot sends updates to users at 19:30 [UTC](time.is/utc)

Once all that's set up, you just need to run the bot with `python Bot.py`. 
