from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler,Filters
from datetime import time
import os
import GraphWeekly
import GraphDaily
import DistrictInfo
import pytz
import MakeMessage
from datetime import timedelta
import WorldTracker

timezone_IST = pytz.timezone('Asia/Kolkata')
rem_time = time(19,30)

with open('token', 'r') as f:
    token = f.read()
updater = Updater(token=token.replace('\n', ''), use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot. Ask me anything")

def graph(update, context):
    args = context.args
    try:
        if args[0].lower()=='weekly':
            if len(args)==1:
                context.bot.send_message(update.effective_chat.id, text="Sorry, I can't recognize those arguments")
            elif len(args)==2:
                if args[1]=='bar':
                    GraphWeekly.update()
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('GraphWeekly.png', 'rb'))
                else:
                    context.bot.send_message(update.effective_chat.id, text="Sorry, I can't recognize those arguments")
            elif len(args)>2:
                if args[1]=='line':
                    countries_str = ''
                    for item in args[2:]:
                        countries_str += item + ' '
                    print(countries_str)
                    countries = [j.strip() for j in countries_str.split(',')]
                    response = WorldTracker.WeeklyAverage(countries)
                    if response=='OK':
                        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('WeeklyAverage.png', 'rb'))
                    else:
                        context.bot.send_message(update.effective_chat.id, text=response)
                else:
                    context.bot.send_message(update.effective_chat.id, text="Sorry, I can not recognize those arguments")
        elif len(args)>=2:
            if args[0].lower()=='daily':
                del args[0]
                if args[0].lower()=='india':
                    if args[1]=='total':
                        args[0] = 2
                        del args[1]
                    elif args[1]=='new':
                        args[0] = 1
                        del args[1]
                    status = GraphDaily.states(args)
                    if status=='Success':
                        context.bot.send_photo(update.effective_chat.id, photo=open('GraphDaily.png', 'rb'))
                        context.bot.send_message(chat_id=update.effective_chat.id, text='Last Updated : Yesterday')
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=status)
                elif args[0].lower()=='world':
                    del args[0]
                    choice = args[0]
                    del args[0]
                    countries_str = ''
                    for item in args:
                        countries_str += item + ' '
                    countries = [j.strip() for j in countries_str.split(',')]
                    if choice=='new':
                        response = WorldTracker.DailyCases(countries)
                    else:
                        response = WorldTracker.CumulativeCases(countries)
                    if response=='OK':
                        context.bot.send_photo(update.effective_chat.id, photo=open('DailyCasesWorld.png', 'rb'))
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
            else:
                context.bot.send_message(update.effective_chat.id, text="Sorry, I can't recognize those arguments")
        elif len(args)==1 and args[0].lower()=='statecodes':
            context.bot.send_message(update.effective_chat.id, text='The following codes are available')
            context.bot.send_message(update.effective_chat.id, text=GraphDaily.getCodes().replace('\t', '    -    '))
        elif len(args)==1 and args[0].lower()=='countrycodes':
            countryList(update, context)
        elif len(args)==0:
            context.bot.send_message(update.effective_chat.id, text="There don't seem to be enough arguments for me to execute that command")
        else:
            context.bot.send_message(update.effective_chat.id, text="Sorry, I can't recognize those arguments")
    except IndexError:
        context.bot.send_message(update.effective_chat.id, text="Sorry, I can't recognize those arguments")


def txtDo(update, context):
    pass

def district(update, context):
    args = context.args
    if len(args)==0:
        context.bot.send_message(update.effective_chat.id, text="There don't seem to be enough arguments for me to execute that command")
    elif len(args)==1:
        Text = DistrictInfo.getDistricts(args[0])
        context.bot.send_message(update.effective_chat.id, text=Text)
    else:
        district_name = ' '.join([args[i].title() for i in range(1,len(args))])
        print(district_name)
        Text = DistrictInfo.getData(args[0], district_name)
        context.bot.send_message(update.effective_chat.id, text=Text)

def help(update, context):
    output_str='''
Here are the available commands

/graph - Plots a graph. Takes multiple parameters. Followed by either 'daily' or 'weekly'. With 'weekly', you have an option of either plot a bar or line chart. Follow weekly by 'bar' to plot the bar chart of India's moving average of new cases. 
Follow it by 'line' and then the countries(separated by commas)to plot the moving average of the choosen countries. For example, type '/graph weekly bar' for a bar chart. For a line chart, type '/graph weekly line India,US,Brazil' 

With daily, you can either choose to plot the cases of India's states or the countries around the world For Indian states, type '/graph daily India total UP MH' where total can be replaced with 'new' for new cases on that day. To view state codes, type '/graph statecodes'. For country codes, type '/graph countrycodes' To plot a graph for countries, type '/graph daily world new US,India'

/update - Fetches the latest data and displays it.
/district - Displays the data for a particular Indian district. Requires a state code and district name. Format: '/district STATECODE DISTRICTNAME'
/help - Whenever you feel lost
'''
    context.bot.send_message(update.effective_chat.id, text=output_str)

def daily(context):
    message = MakeMessage.getString()
    context.bot.send_message(chat_id=my_id, text=message[0])
    context.bot.send_message(chat_id=my_id, text=message[1])
    context.bot.send_message(chat_id=my_id, text=message[2])

def upd(update, context):
    daily(context)

def countryList(update, context):
    countries_list_str = 'Here are the available countries - \n\n'
    with open('countries.txt', 'r') as f:
        countries_list_str += f.read()
    context.bot.send_message(chat_id=update.effective_chat.id, text=countries_list_str)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CommandHandler('graph', graph))
dispatcher.add_handler(CommandHandler('update', upd))
dispatcher.add_handler(CommandHandler('district', district))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('country', countryList))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, txtDo))
j.run_repeating(daily,interval=timedelta(days=1), first=rem_time)
updater.start_polling()
updater.idle()
