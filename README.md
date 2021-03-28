# Covid19 Telegram Bot
 A general purpose bot for accessing the latest information about Covid19 in India
 
 ## Sources
 
1. [Covid19 India](https://github.com/covid19india/api)
2. [Pomber Covid19](https://github.com/pomber/covid19)
 
 ## How to use
 
 The Bot can be found under @MyTelegramCovidBot on Telegram. Say hello to it from us!

## Available commands 

Here are the available commands

### `/graph` 

Plots a graph. Takes multiple parameters. Followed by either 'daily' or 'weekly'. With 'weekly', you have an option of either plot a bar or line chart. Follow weekly by 'bar' to plot the bar chart of India's moving average of new cases. 
Follow it by 'line' and then the countries(separated by commas)to plot the moving average of the choosen countries. For example, type `/graph weekly bar` for a bar chart. For a line chart, type `/graph weekly line India,US,Brazil`

With daily, you can either choose to plot the cases of India's states or the countries around the world For Indian states, type `/graph daily India total UP MH` where total can be replaced with `new` for new cases on that day. To view state codes, type '/statecodes'. For country codes, type `/countrycodes` To plot a graph for countries, type `/graph daily world new US,India`

### `/update` 

Fetches the latest data and displays it.

### `/district`

Displays the data for a particular Indian district. Requires a state code and district name. Format: '/district STATECODE DISTRICTNAME. If DISTRICTNAME is not provided, all districts in the provided STATECODE are displayed '

### `/factcheck` 

Sends you the latest Factcheck

### `/help` 

Whenever you feel lost

### `/helpmode`

Still feel confused? Use our easy and intuitive prompt based query builder by typing `/helpmode`. Recommended for new users

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

## More?

Visit our website [here](https://thetrio.github.io/Covid19-India-Telegram-Bot/)
