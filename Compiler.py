from Token import Token
from Command import Command
import requests
import nltk

class Compiler:
    def get_command(input_str, args):
        input_str = input_str.strip()
        tags = nltk.tag.pos_tag(input_str.split())
        command_params = []
        countries = []
        for param in nltk.tag.pos_tag(input_str.split()):
            if param[0].startswith('/'):
                continue
            elif param[0].lower() in args:
                command_params.append(Token(param[0]))
            elif param[1]=='NNP':
                countries.append(param[0])
        return Command(command_params, countries)