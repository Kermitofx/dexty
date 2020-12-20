# Copyright (C) 2018-2019 Amano Team <contact@amanoteam.ml>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from amanobot.namedtuple import InlineKeyboardMarkup

import keyboard
from config import bot, version, bot_username, git_repo
from db_handler import cursor
from get_strings import strings, Strings

async def start(msg):
    if msg.get('text'):
        strs = Strings(msg['chat']['id'])

        if msg['text'] == '/start' or msg['text'] == '!start' or msg['text'].split()[
            0] == '/start@' + bot_username or msg['text'] == '/start start':

            if msg['chat']['type'] == 'private':
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [dict(text=strs.get('commands_button'), callback_data='all_cmds')] +
                    [dict(text=strs.get('infos_button'), callback_data='infos')],
                    [dict(text=strs.get('lang_button'), callback_data='change_lang')] +
                    [dict(text=strs.get('add_button'), url='https://t.me/{}?startgroup=new'.format(bot_username))]
                ])
                smsg = strs.get('pm_start_msg')
            else:
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [dict(text=strs.get('start_pm_button'), url='https://t.me/{}?start=start'.format(bot_username))]
                ])
                smsg = strs.get('start_msg')

            await bot.sendMessage(msg['chat']['id'], smsg,
                                  reply_to_message_id=msg['message_id'], reply_markup=kb)
            return True


    elif msg.get('data') and msg.get('message'):
        strs = Strings(msg['message']['chat']['id'])

        cmds_back = InlineKeyboardMarkup(inline_keyboard=[
            [dict(text=strs.get('back_button'), callback_data='all_cmds')]
        ])

        start_back = InlineKeyboardMarkup(inline_keyboard=[
            [dict(text=strs.get('back_button'), callback_data='start_back')]
        ])

        if msg['data'] == 'tools_cmds':
            await bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']),
                                      text='''*Tools:*

/climate - Displays weather information.
/coub - Search for small animations.
/echo - Repeat the entered text.
/gif - GIF Search.
/git - It sends the information of a user of GitHub.
/html - Repeats text or informed using HTML.
/ip - Displays information about an IP/domain.
/jsondump - Sends the json message.
/mark - Repeats the entered text using Markdown.
/print - Submit a print from a website.
/pypi - PyPI Module Search.
/r - Reddit Topic Search
/request - It makes a request to a web site.
/shorten - Shorten a URL.
/token - It displays information from the token to the bot .
/tr - Translate a text.
/yt - Search videos on YouTube.
/ytdl - Download audio from a video on YouTube.''',
                                      parse_mode='Markdown',
                                      reply_markup=cmds_back)
            return True


        elif msg['data'] == 'admin_cmds':
            await bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']),
                                      '''*Administration Commands:*

/ban - Bans a user.
/config - Send a settings menu.
/defrules - Define group rules.
/kick - Kicks a user.
/mute - Restricts a user.
/pin - Pin a message to the group.
/title - Define the title of the group.
/unban - Unbans the user.
/unmute - Unmutes a user.
/unpin - Unpins a message in the group.
/unwarn - Remove user warnings.
/warn - Warns a user.
/welcome - To Set welcome message.''',
                                      parse_mode='Markdown',
                                      reply_markup=cmds_back)
            return True


        elif msg['data'] == 'user_cmds':
            await bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']),
                                      '''*Commands for normal users:*

/admins - Show list of chat admins.
/dados - Send a random number from 1 to 6.
/bug - To Report a bug of the bot to the owner.
/id - To get the Id of the user.
/ping - Responds with a ping message.
/rules - Displays group rules.
/roleta - To play Russian Roulette.''',
                                      parse_mode='Markdown',
                                      reply_markup=cmds_back)
            return True


        elif msg['data'] == 'start_back':
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [dict(text=strs.get('commands_button'), callback_data='all_cmds')] +
                [dict(text=strs.get('infos_button'), callback_data='infos')],
                [dict(text=strs.get('lang_button'), callback_data='change_lang')] +
                [dict(text=strs.get('add_button'), url='https://t.me/{}?startgroup=new'.format(bot_username))]
            ])
            await bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']),
                                      strs.get('pm_start_msg'),
                                      reply_markup=kb)
            return True


        elif msg['data'] == 'change_lang':
            langs_kb = InlineKeyboardMarkup(inline_keyboard=
                                            [[dict(text='{lang_flag} {lang_name}'.format(**strings[x]),
                                                   callback_data='set_lang ' + x)] for x in strings] +
                                            [[dict(text=strs.get('back_button'), callback_data='start_back')]]
                                            )
            await bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']),
                                      "Select your prefered lang below:",
                                      reply_markup=langs_kb)
            return True


        elif msg['data'].split()[0] == 'set_lang':
            cursor.execute('UPDATE users SET chat_lang = ? WHERE user_id = ?',
                           (msg['data'].split()[1], msg['message']['chat']['id']))
            usr_lang = Strings(msg['message']['chat']['id'])
            start_back = InlineKeyboardMarkup(inline_keyboard=[
                [dict(text=usr_lang.get('back_button'), callback_data='start_back')]
            ])
            await bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']),
                                      usr_lang.get('lang_changed'),
                                      reply_markup=start_back)
            return True


        elif msg['data'] == 'all_cmds':
            await bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']),
                                      'Select a command category to view.\n\nIf you need help with the bot or have any suggestions go to @KeralasBots',
                                      reply_markup=keyboard.all_cmds)
            return True


        elif msg['data'] == 'infos':
            await bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']),
                                      '''• JOKER

Version: {version}
Source Code: <a href="{sourcelink}">Here</a>
Developers: <a href="https://github.com/Anandpskerala">Mia Team</>
Owner: <a href="tg://user?id=646146866">Anand</>

Partnerships:
 » <a href="https://t.me/AmanoTeam">Amano Team</>

©2019 - <a href="https://t.me/KeralasBots">Mia Team™</>'''.format(version=version, sourcelink=git_repo[0]),
                                      parse_mode='html',
                                      reply_markup=start_back,
                                      disable_web_page_preview=True)
            return True
