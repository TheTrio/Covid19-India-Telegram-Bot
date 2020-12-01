# Covid19 Telegram Bot
 A general purpose bot for accessing the latest information about Covid19 in India
 
 ## How to use
 
You're expected to have an API Token for your Telegram chat bot, and that is to be saved in a file named `token`, located in the same directory as the rest of these files. If you're not sure what that means, please read [this](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) quick and easy tutorial.

Once that's set up, you just need to run the bot with `python Bot.py`. 

## Available commands 

Here are the available commands

### `/graph` 

Plots a graph. Takes multiple parameters. Followed by either `daily` or `weekly`. 

With `weekly`, you have an option of either plot a bar or line chart. Follow weekly by `bar` to plot the bar chart of India's moving average of new cases. 
Follow it by `line` and then the countries(separated by commas)to plot the moving average of the choosen countries. For example, type `/graph weekly bar` for a bar chart. For a line chart, type `/graph weekly line India,US,Brazil` 

With daily, you can either choose to plot the cases of India's states or the countries around the world For Indian states, type `/graph daily India total UP MH` where total can be replaced with `new` for new cases on that day. To view state codes, type `/graph statecodes`. For country codes, type `/graph countrycodes` To plot a graph for countries, type `/graph daily world new US,India`

### `/update` - Fetches the latest data and displays it.
### `/district` - Displays the data for a particular Indian district. Requires a state code and district name. Format: '/district STATECODE DISTRICTNAME'
### `/help`- Whenever you feel lost

