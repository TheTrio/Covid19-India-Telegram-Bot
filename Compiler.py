from Token import Token
from Command import Command
import nltk
from Utils import Utils

class Compiler:
    def get_command(input_str, args, countries_list, states_list):
        input_str = input_str.strip()
        tags = nltk.tag.pos_tag(input_str.split())
        command_params = []
        countries = []
        country_found = False
        for param in nltk.tag.pos_tag(input_str.split()):
            print(param)
            if param[0].startswith('/') or param[0]=='graph':
                continue
            elif param[0].lower() in args:
                command_params.append(Token(param[0]))
            elif Utils.is_country(param[0], countries_list):
                countries.append(param[0])
                country_found = True
                print('hello')
            elif Utils.is_state(param[0], states_list):
                countries.append(param[0])
            elif param[1]=='NNP':
                countries.append(param[0])
        return Command(command_params, countries, country_found)