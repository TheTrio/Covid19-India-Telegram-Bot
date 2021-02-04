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
from Utils import Utils
import json
from User import User
from Compiler import Compiler

timezone_IST = pytz.timezone('Asia/Kolkata')
rem_time = time(19,30)
my_id = 1143044528
states_codes = {
    'Andaman and Nicobar Islands':'AN',
    'Andhra Pradesh':'AP',
    'Arunachal Pradesh':'AR',
    'Assam':'AS',
    'Bihar':'BR',
    'Chandigarh':'CH',
    'Chhattisgarh':'CT',
    'Daman and Diu':'DD',
    'Delhi':'DL',
    'Dadra and Nagar Haveli':'DN',
    'Goa': 'GA',
    'Gujarat':'GJ',
    'Himachal Pradesh':'HP',
    'Haryana':'HR',
    'Jharkhand':'JH',
    'Ladakh':'LA',
    'Karnataka':'KA',
    'Kerala':'KL',
    'Lakshadweep':'LD',
    'Maharashtra':'MH',
    'Meghalaya':'ML',
    'Manipur':'MN',
    'Madhya Pradesh':'MP',
    'Mizoram':'MZ',
    'Nagaland':'NL',
    'Odisha':'OR',
    'Punjab':'PB',
    'Puducherry':'PY',
    'Rajasthan':'RJ',
    'Sikkim':'SK',
    'Telangana':'TG',
    'Tamil Nadu':'TN',
    'Tripura':'TR',
    'Uttar Pradesh':'UP',
    'Uttarakhand':'UT',
    'West Bengal':'WB',
    'Jammu and Kashmir':'JK',
    'India':'TT'
}
with open('countries.txt') as f:
    countries_list = list(map(lambda x : x.replace('\n', ''), f.readlines()))

with open('states.txt') as f:
    states_list = list(map(lambda x : x.replace('\n', ''), f.readlines()))
with open('token', 'r') as f:
    token = f.read()
updater = Updater(token=token.replace('\n', ''), use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue
running_users = {}
error_str = "Sorry, I couldn't understand you. Please try and type exactly what you want. If I'm still unable to understand, you can try using /helpMode"
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
    current_user = {
        'fname':update.effective_user.first_name,
        'lname':update.effective_user.last_name,
        'username':update.effective_user.username,
        'id':update.effective_user.id
    }
    if current_user['id'] not in running_users:
        running_users[current_user['id']] = User(current_user['fname'], current_user['lname'], current_user['username'])
    with open('Users.json') as f:
        users = json.load(f)
    newUser = True
    for user in users['users']:
        if user['id']==current_user['id']:
            newUser = False
            break
    if newUser:
        with open('Users.json', 'w') as f:
            users['users'].append(current_user)
            json.dump(users, f)
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_str, parse_mode='MarkdownV2')

def graph(update, context):
    args = context.args
    makeGraph(update, context, args)

def statecodes(update,context):
    context.bot.send_message(update.effective_chat.id, text='The following codes are available')
    context.bot.send_message(update.effective_chat.id, text=GraphDaily.getCodes().replace('\t', '    -    '))

def countrycodes(update, context):
    countryList(update, context)

def convert_to_code(state):
    if len(state)==2:
        return state
    else:
        return states_codes[state]

def makeGraph(update, context, args, parse=True):
    command_str = ' '.join(args)
    command = Compiler.get_command(command_str, ['daily', 'india', 'new', 'line', 'bar', 'total', 'world', 'weekly']).get_sorted_command()
    command.convert()
    args_updated = []
    for token in command.command:
        args_updated.append(token.name)
    countries_comma_str = ','.join(command.countries)
    if len(countries_comma_str)!=0:
        args_updated.append(countries_comma_str)
    args = args_updated
    print(args)
    try:
        if args[0].lower()=='weekly':
            if len(args)==1:
                context.bot.send_message(update.effective_chat.id, text=error_str)
            elif len(args)==2:
                if args[1]=='bar':
                    print('hey')
                    GraphWeekly.update()
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('GraphWeekly.png', 'rb'))
                else:
                    context.bot.send_message(update.effective_chat.id, text=error_str)
            elif len(args)>2:
                if args[1]=='line':
                    countries_str = ''
                    if parse:
                        for item in args[2:]:
                            countries_str += item + ' '
                        countries = [j.strip() for j in countries_str.split(',')]
                    else:
                        countries = args[2:]
                    countries = list(map(lambda x: Utils.find_closest_match(update, context, countries_list, x)[0], countries))
                    response = WorldTracker.WeeklyAverage(countries)
                    if response=='OK':
                        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('WeeklyAverage.png', 'rb'))
                    else:
                        context.bot.send_message(update.effective_chat.id, text=response)
                else:
                    context.bot.send_message(update.effective_chat.id, text=error_str)
        elif len(args)>=2:
            if args[0].lower()=='daily':
                del args[0]
                if args[0].lower()=='india':
                    choice=args[1]
                    
                    if parse:
                        args = ' '.join(args[2:])
                        args = list(map(lambda z: z.strip(), filter(lambda x: len(x.strip())>0,args.split(','))))
                    else:
                        args = args[2:]
                    args = list(map(lambda x : Utils.find_closest_state(update,context, states_list, x), args))
                    args = list(map(convert_to_code, args))
                    status = GraphDaily.states(args, choice)
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
                    countries = list(map(lambda x: Utils.find_closest_match(update, context, countries_list, x)[0], countries))
                    print(countries)
                    if choice=='new':
                        response = WorldTracker.DailyCases(countries)
                    else:
                        response = WorldTracker.CumulativeCases(countries)
                    if response=='OK':
                        context.bot.send_photo(update.effective_chat.id, photo=open('DailyCasesWorld.png', 'rb'))
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
            else:
                context.bot.send_message(update.effective_chat.id, text=error_str)
        elif len(args)==0:
            context.bot.send_message(update.effective_chat.id, text="Hello! It looks like you haven't typed anything! Please try and type exactly what you want. If I'm still unable to understand, you can try using /helpMode")
        else:
            context.bot.send_message(update.effective_chat.id, text=error_str)
    except IndexError:
        context.bot.send_message(update.effective_chat.id, text=error_str)

def txtDo(update, context):
    pass

def district(update, context):
    args = context.args
    if len(args)==0:
        context.bot.send_message(update.effective_chat.id, text="There don't seem to be enough arguments for me to execute that command")
    elif len(args)==1:
        args[0] = Utils.find_closest_state(update, context, states_list, args[0])
        args[0] = convert_to_code(args[0])
        Text = DistrictInfo.getDistricts(args[0])
        context.bot.send_message(update.effective_chat.id, text=Text)
    else:
        makeDistrict(update, context, args)

def makeDistrict(update, context, args):
    district_name = ' '.join([args[i].title() for i in range(1,len(args))])
    args[0] = Utils.find_closest_state(update, context, states_list, args[0])
    args[0] = convert_to_code(args[0])
    district_name = Utils.find_closest_match(update, context, DistrictInfo.get_district_list(args[0]), district_name)[0]
    print(args[0], district_name[0])
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
    if not results:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry, I was unavailable to find any certified factchecks for your query")
    else:
        for result in results[0:3]:
            context.bot.send_message(chat_id=update.effective_chat.id, text=result['link'])

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

def reset_user(user):
    user.tree = Tree()
    user.query_string = ''
    user.help_mode = False


def txtDo(update, context):
    current_user = running_users[update.effective_user.id]
    if current_user.help_mode:
        print('hey')
        inputStr = update.message.text_markdown
        if inputStr.lower() == 'exit':
            reset_user(current_user)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Exited from HelpMode\. If you want to enable it, type `/helpmode`', parse_mode='MarkdownV2')
            return
        flag = False
        choosen = None
        for choice in current_user.tree.children:
            if choice.name.lower() == inputStr.lower():
                flag = True
                choosen = choice
                break
        if len(current_user.tree.children)==0 and current_user.tree.name == 'district':
            newArgs = current_user.query_string.strip().split(' ')
            newArgs.extend(inputStr.strip().split(' '))
            executeCommand(update, context, newArgs)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Helpmode has been set to false\. If you want to generate another query, just type `/helpmode`', parse_mode='MarkdownV2')
            reset_user(current_user)
            return
        elif len(current_user.tree.children)==0 and current_user.tree.name=='factcheck':
            newArgs = current_user.query_string.strip().split(' ')
            newArgs.extend(inputStr.strip().split(' '))
            executeCommand(update, context, newArgs)
            reset_user(current_user)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Helpmode has been set to false\. If you want to generate another query, just type `/helpmode`', parse_mode='MarkdownV2')
            return
        elif len(current_user.tree.children)==0:
            inputStr = re.sub('\s*,\s*', ',', inputStr)
            newArgs = current_user.query_string.strip().split(' ')
            newArgs.extend(inputStr.split(','))
            print(newArgs)
            reset_user(current_user)
            executeCommand(update, context, newArgs)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Helpmode has been set to false\. If you want to generate another query, just type `/helpmode`', parse_mode='MarkdownV2')
            return
        elif (not flag):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Not a valid choice. Please try again')
        else:
            current_user.query_string += choice.command + ' '
            current_user.tree = choice
        if len(current_user.tree.children)==0:
            if current_user.tree.name=='new' or current_user.tree.name=='total':
                outputStr = '''
Type a ,(comma) separated list of states/countries you want to plot. For example, if you want to plot Maharashtra and Delhi, type MH,DL

Not aware of the state/country codes? Type /countrycodes or /statecodes as per your need
                '''
                context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr)
            elif current_user.tree.name=='line':
                outputStr = '''
Type a ,(comma) separated list of countries you want to plot. For example, if you want to plot India and Brazil, type India,Brazil

Not aware of the country codes? Type /countrycodes
                '''
                context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr)
            elif current_user.tree.name=='district':
                outputStr = '''
Enter the statecode, followed by the name of the district you wish to select\. For example, if you want to select Agra, type `UP Agra`

Not aware of the state codes? Type /statecodes to view them\. 

If you wish to view the names of all districts in a particular state, type `/district statecode`\. For example, `/district UP`
                '''
                context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr,parse_mode='MarkdownV2')
            elif current_user.tree.name=='factcheck':
                outputStr = '''
Please type what you want to factcheck about\. For example, if you want factcheck conspiracy theories relating 5G to the pademic, you can type `5G`\. If you have multiple queries, separate them by a space\. 
                '''
                context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr,parse_mode='MarkdownV2')
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your requested command is `{current_user.query_string}`', parse_mode='MarkdownV2')
                executeCommand(update, context, current_user.query_string.strip().split(' '))
                reset_user(current_user)
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'Helpmode has been set to false\. If you want to generate another query, just type `/helpmode`', parse_mode='MarkdownV2')
        else:
            outputStr = 'Here are your available options. Just type the keyword you want to choose.\n'
            context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr)
            outputStr = ''
            for child in current_user.tree.children:
                outputStr += child.getHelp() + '\n\n'
            context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr, parse_mode='MarkdownV2')
def helpmode(update, context):
    current_user_obj = {
        'fname':update.effective_user.first_name,
        'lname':update.effective_user.last_name,
        'username':update.effective_user.username,
        'id':update.effective_user.id
    }
    if current_user_obj['id'] not in running_users:
        running_users[current_user_obj['id']] = User(current_user_obj['fname'], current_user_obj['lname'], current_user_obj['username'])
    
    current_user = running_users[update.effective_user.id]
    current_user.help_mode = not current_user.help_mode
    outputStr = '''
Hello. I'm going to guide you in building your query. If at any point you'd like to quit, just type exit. 

Here are your available options. Just type the keyword you want to choose.\n
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr)
    outputStr = ''
    if current_user.help_mode:
        for child in current_user.tree.children:
            outputStr += child.getHelp() + '\n\n'
        context.bot.send_message(chat_id=update.effective_chat.id, text=outputStr, parse_mode='MarkdownV2')
    if not current_user.help_mode:
        reset_user(current_user)

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
