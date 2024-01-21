import colorama
import time
import re
import os
import requests
import json

def auto_mkdir(*paths: str) -> None:
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)


def arrange_text(text):
    return re.sub('\/:*?"<>|.', ' ', text)


def print_detail(memo='', user=None, guild=None, channel=None, obj=None) -> None:

    flush = False

    colorama.init()

    if memo == 'INFO':
        mcolor = colorama.Fore.GREEN
    elif memo == 'WARN':
        mcolor = colorama.Fore.RED
    elif memo == 'ERROR':
        mcolor = colorama.Fore.RED + colorama.Style.BRIGHT
    elif memo == 'COMPLETENESS':
        flush = True
        mcolor = colorama.Fore.CYAN
    else:
        mcolor = colorama.Fore.CYAN

    class Formate:
        name = ''
        discriminator = ''
        id = ''

    if user == None:
        user = Formate
    if guild == None:
        guild = Formate
    if channel == None:
        channel = Formate
        

    def fill(string, length: int) -> str:
        if string == '':
            return ' ' * length
        else:
            import unicodedata
            string = str(string)
            leng = 0
            for char in string:
                if unicodedata.east_asian_width(char) == 'W':
                    leng += 2
                else:
                    leng += 1
        if leng < length:
            gap = length - leng
            string = ' ' * gap + string

        return string
 
    try:
        print(f'{colorama.Style.DIM}[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]{colorama.Style.RESET_ALL}{mcolor}[{fill(memo, 5)}]{colorama.Style.RESET_ALL}{colorama.Fore.BLUE}[{fill(f"{user.name}#{user.discriminator}", 20)}({fill(user.id, 19)})][{fill(guild.name, 20)}({fill(guild.id, 19)})][{fill(getattr(channel, "name", ""), 20)}({fill(channel.id, 19)})]{colorama.Style.RESET_ALL}\n{obj}\n', flush=flush)
    except Exception as e:
        print(e)


def split_str_to_list(text: str, size: int) -> list:
    text_list = []
    if text != '':
        while True:
            text_list.append(text[:size])
            text = text[size + 1:]
            if text == '':
                break
    else:
        text_list = ['']

    print_detail(memo='INFO', obj=f'Form list: "{text_list}"')

    return text_list

def get_file(url: str):
    return requests.get(url, headers={'user-agent': 'Mozilla/5.0'}).content