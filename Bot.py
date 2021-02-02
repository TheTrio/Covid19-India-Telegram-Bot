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
from FactCheck import find
from Tree import Tree
import re

timezone_IST = pytz.timezone('Asia/Kolkata')
rem_time = time(19,30)
my_id = 1143044528

with open('token', 'r') as f:
    token = f.read()
updater = Updater(token=token.replace('\n', ''), use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue
helpMode = False
tree = Tree()
queryString = ''
help_str = '''
Here are the available commands. 

/graph - Plots a graph. Takes multiple parameters. Followed by either 'daily' or 'weekly'. With 'weekly', you have an option of either plot a bar or line chart. Follow weekly by 'bar' to plot the bar chart of India's moving average of new cases. 
Follow it by 'line' and then the countries(separated by commas)to plot the moving average of the choosen countries. For example, type '/graph weekly bar' for a bar chart. For a line chart, type '/graph weekly line India,US,Brazil' 

With daily, you can either choose to plot the cases of India's states or the countries around the world For Indian states, type '/graph daily India total UP MH' where total can be replaced with 'new' for new cases on that day. To view state codes, type '/statecodes'. For country codes, type '/countrycodes' To plot a graph for countries, type '/graph daily world new US,India'

/update - Fetches the latest data and displays it.

/district - Displays the data for a particular Indian district. Requires a state code and district name. Format: '/district STATECODE DISTRICTNAME. If DISTRICTNAME is not provided, all districts in the provided STATECODE are displayed '

/factcheck - Sends you the latest Factcheck

/help - Whenever you feel lost

Still feel confused? Use our easy and intuitive prompt based query builder by typing /helpmode. Recommended for new users
'''

welcome_str = '''
Hello\! I'm an open source Covid19 Bot and I'm here to help\. 

I take a multitude of queries as input and present you with the desired output\. To take a detailed look at the various commands available, type `/help`\. 

Don't have the time to read? Use our easy and intuitive query builder by typing `/helpmode`

You can read more at my website [here](https://thetrio.github.io/Covid19-India-Telegram-Bot/)\.

If you encounter any bugs or wish to tell us anything, please contact us using the aformentioned website\.

Happy Tinkering\!
Covid19 Bot
'''
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_str, parse_mode='MarkdownV2')

def graph(update, context):
    args = context.args
    makeGraph(update, context, args)

def statecodes(update,context):
    context.bot.send_message(update.effective_chat.id, text='The following codes are available')
    context.bot.send_message(update.effective_chat.id, text=GraphDaily.getCodes().replace('\t', '    -    '))

def countrycodes(update, context):
    countryList(update, context)

def makeGraph(update, context, args, parse=True):
    try:
        if args[0].lower()=='weekly':
            if len(args)==1:
                context.bot.send_message(update.effective_chat.id, text="Sorry, I can't recognize those arguments")
            elif len(args)==2:
                if args[1]=='bar':
                    print('hey')
                    GraphWeekly.update()
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('GraphWeekly.png', 'rb'))
                else:
                    context.bot.send_message(update.effective_chat.id, text="Sorry, I can't recognize those arguments")
            elif len(args)>2:
                if args[1]=='line':
                    countries_str = ''
                    if parse:
                        for item in args[2:]:
                            countries_str += item + ' '
                        countries = [j.strip() for j in countries_str.split(',')]
                    else:
                        countries = args[2:]
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
                    if parse:
                        for item in args:
                            countries_str += item + ' '
                        countries = [j.strip() for j in countries_str.split(',')]
                    else:
                        countries = args
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
        makeDistrict(update, context, args)

def makeDistrict(update, context, args):
    print(args)
    district_name = ' '.join([args[i].title() for i in range(1,len(args))])
    print(district_name)
    Text = DistrictInfo.getData(args[0], district_name)
    context.bot.send_message(update.effective_chat.id, text=Text)

def help(update, context):
    
    context.bot.send_message(update.effective_chat.id, text=help_str)

def daily(context):
    message = MakeMessage.getString()
    context.bot.send_message(chat_id=my_id, text=message[0])
    context.bot.send_message(chat_id=my_id, text=message[1])
    context.bot.send_message(chat_id=my_id, text=message[2])

def upd(update, context):
    message = MakeMessage.getString()
    context.bot.send_message(chat_id=update.effective_chat.id, text=message[0])
    context.bot.send_message(chat_id=update.effective_chat.id, text=message[1])
    context.bot.send_message(chat_id=update.effective_chat.id, text=message[2])

def countryList(update, context):
    countries_list_str = 'Here are the available countries - \n\n'
    with open('countries.txt', 'r') as f:
        countries_list_str += f.read()
    context.bot.send_message(chat_id=update.effective_chat.id, text=countries_list_str)

def makefactcheck(update, context,queries):
    queries.append('covid')
    queries.append('coronavirus')
    results = find(queries)
    for result in results[0:3]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=result['unescapedUrl'])

def factcheck(update, context):
    queries = context.args
    makefactcheck(update, context, queries)

def executeCommand(update, context, args):
    if args[0]=='/graph':
        makeGraph(update, context, args[1:], False)
    elif args[0]=='/help':
        context.bot.send_message(chat_id=update.effective_chat.id, text=help_str)
    elif args[0]=='/update':
        upd(update,context)
    elif args[0]=='/district':
        makeDistrict(update, context,args[1:])
    elif args[0]=='/factcheck':
        print(args)
        makefactcheck(update, context, args[1:])

def txtDo(update, context):
    global tree
    global queryString
    global helpMode
    if helpMode:
        inputStr = update.message.text_markdown
        if inputStr.lower() == 'exit':
            tree = Tree()
            queryString = ''
            helpMode = False
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Exited from HelpMode\. If you want to enable it, type `/helpmode`', parse_mode='MarkdownV2')
            return
        flag = False
        choosen = None
        for choice in tree.children:
            if choice.name.lower() == inputStr.lower():
                flag = True
                choosen = choice
                break
        if len(tree.children)==0 and tree.name == 'district':
            newArgs = queryString.strip().split(' ')
            newArgs.extend(inputStr.strip().split(' '))
            executeCommand(update, context, newArgs)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Helpmode has been set to false\. If you want to generate another query, just type `/helpmode`', parse_mode='MarkdownV2')
            helpMode  = False
            tree = Tree()
            queryString = ''
            return
        elif len(tree.children)==0 and tree.name=='factcheck':
            newArgs = queryString.strip().split(' ')
            newArgs.extend(inputStr.strip().split(' '))
            executeCommand(update, context, newArgs)
            helpMode  = False
            tree = Tree()
            queryString = ''
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Helpmode has been set to false\. If you want to generate another query, just type `/helpmode`', parse_mode='MarkdownV2')

            return
        elif len(tree.children)==0:
            inputStr = re.sub('\s+', '', inputStr)
            newArgs = queryString.strip().split(' ')
            newArgs.extend(inputStr.split(','))
            print(newArgs)
            helpMode  = False
            tree = Tree()
            queryString = ''
            executeCommand(update, context, newArgs)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Helpmode has been set to false\. If you want to generate another query, just type `/helpmode`', parse_mode='MarkdownV2')
            return
        elif (not flag):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Not a valid choice. Please try again')
        else:
            queryString += choice.command + ' '
            tree = choice
        if len(tree.children)==0:
            if tree.name=='new' or tree.name=='total':
                outputStr = '''
Type a ,(comma) separated list of states/countries you want to plot. For example, if you want to plot Maharashtra and Delhi, type MH,DL

Not aware of the state/country codes? Type /countrycodes or /statecodes as per your need
                '''
                context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr)
            elif tree.name=='line':
                outputStr = '''
Type a ,(comma) separated list of countries you want to plot. For example, if you want to plot India and Brazil, type India,Brazil

Not aware of the country codes? Type /countrycodes
                '''
                context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr)
            elif tree.name=='district':
                outputStr = '''
Enter the statecode, followed by the name of the district you wish to select\. For example, if you want to select Agra, type `UP Agra`

Not aware of the state codes? Type /statecodes to view them\. 

If you wish to view the names of all districts in a particular state, type `/district statecode`\. For example, `/district UP`
                '''
                context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr,parse_mode='MarkdownV2')
            elif tree.name=='factcheck':
                outputStr = '''
Please type what you want to factcheck about\. For example, if you want factcheck conspiracy theories relating 5G to the pademic, you can type `5G`\. If you have multiple queries, separate them by a space\. 
                '''
                context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr,parse_mode='MarkdownV2')
            else:
                tree = Tree()
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your requested command is `{queryString}`', parse_mode='MarkdownV2')
                executeCommand(update, context, queryString.strip().split(' '))
                queryString = ''
                helpMode = False
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'Helpmode has been set to false\. If you want to generate another query, just type `/helpmode`', parse_mode='MarkdownV2')
        else:
            outputStr = 'Here are your available options. Just type the keyword you want to choose.\n'
            context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr)
            outputStr = ''
            for child in tree.children:
                outputStr += child.getHelp() + '\n\n'
            context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr, parse_mode='MarkdownV2')
def helpmode(update, context):
    global queryString
    global tree
    global helpMode
    helpMode = not helpMode
    outputStr = '''
Hello. I'm going to guide you in building your query. If at any point you'd like to quit, just type exit. 

Here are your available options. Just type the keyword you want to choose.\n
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr)
    outputStr = ''
    if helpMode:
        for child in tree.children:
            outputStr += child.getHelp() + '\n\n'
        context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr, parse_mode='MarkdownV2')
    if not helpMode:
        queryString  =  ''
        tree = Tree()

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CommandHandler('graph', graph))
dispatcher.add_handler(CommandHandler('update', upd))
dispatcher.add_handler(CommandHandler('district', district))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('country', countryList))
dispatcher.add_handler(CommandHandler('factcheck', factcheck))
dispatcher.add_handler(CommandHandler('helpmode', helpmode))
dispatcher.add_handler(CommandHandler('statecodes', statecodes))
dispatcher.add_handler(CommandHandler('countrycodes', countrycodes))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, txtDo))
j.run_repeating(daily,interval=timedelta(days=1), first=rem_time)
updater.start_polling()
updater.idle()
