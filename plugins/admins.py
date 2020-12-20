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

import json
import time

from amanobot.exception import TelegramError, NotEnoughRightsError
from amanobot.namedtuple import InlineKeyboardMarkup

from config import bot, bot_id, sudoers
from db_handler import conn, cursor


async def is_admin(chat_id, user_id, reply_id=None):
    if int(chat_id) < 0:  # Groups and supergoups IDs.
        dic = {}
        cursor.execute('SELECT cached_admins FROM chats WHERE chat_id = ?', (int(chat_id),))
        adms = cursor.fetchone()[0]
        if adms:
            cached_admins = json.loads(adms)
        else:
            cached_admins = {'expires': 0}

        if cached_admins['expires'] > time.time():
            adm_id = cached_admins['admins_list']
        else:
            adms = await bot.getChatAdministrators(chat_id)
            adm_id = []
            for ids in adms:
                adm_id.append(ids['user']['id'])
            cursor.execute('UPDATE chats SET cached_admins = ? WHERE chat_id = ?', (json.dumps(dict(admins_list=adm_id, expires=int(time.time()) + 1200)), chat_id))
            conn.commit()

        if user_id in adm_id or user_id in sudoers:
            dic['user'] = True
        else:
            dic['user'] = False

        if reply_id in adm_id:
            dic['reply'] = True
        else:
            dic['reply'] = False

        if bot_id in adm_id:
            dic['bot'] = True
        else:
            dic['bot'] = False

    else:  # User IDs.
        dic = dict(user=False, reply=False, bot=False)

    return dic


async def admins(msg):
    if msg.get('text'):
        if msg['text'].split()[0] == '/ban' or msg['text'].split()[0] == '!ban':
            if msg['chat']['type'] == 'private':
                await bot.sendMessage(msg['chat']['id'], 'This command works only in groups. ¯\\_(ツ)_/¯')
            else:
                if msg.get('reply_to_message'):
                    reply_id = msg['reply_to_message']['from']['id']
                    reply_name = msg['reply_to_message']['from']['first_name']
                elif len(msg['text'].split()) > 1:
                    u_id = msg['text'].split()[1]
                    try:
                        get = await bot.getChat(u_id)
                        reply_id = get['id']
                        reply_name = get['first_name']
                    except (TelegramError, KeyError):
                        await bot.sendMessage(msg['chat']['id'],
                                              'Invalid or unknown ID. Use format: /ban ID of the user',
                                              reply_to_message_id=msg['message_id'])
                        return
                else:
                    reply_id = None

                adm = await is_admin(msg['chat']['id'], msg['from']['id'], reply_id)

                if adm['user']:
                    try:
                        int(reply_id)
                    except (TypeError, ValueError):
                        return await bot.sendMessage(msg['chat']['id'], 'Reply to someone s message or enter his ID.',
                                                     reply_to_message_id=msg['message_id'])
                    if adm['bot']:
                        if adm['reply']:
                            await bot.sendMessage(msg['chat']['id'], 'This one is an admin here.',
                                                  reply_to_message_id=msg['message_id'])
                        else:
                            await bot.kickChatMember(msg['chat']['id'], reply_id)
                            await bot.sendMessage(msg['chat']['id'], f'{msg["from"]["first_name"]} banned {reply_name}!',
                                                  reply_to_message_id=msg['message_id'])
                    else:
                        await bot.sendMessage(msg['chat']['id'], 'Hey, I am not an admin here.',
                                              reply_to_message_id=msg['message_id'])


        elif msg['text'].split()[0] == '/kick' or msg['text'].split()[0] == '!kick':
            if msg['chat']['type'] == 'private':
                await bot.sendMessage(msg['chat']['id'], 'This command works only in groups. ¯\\_(ツ)_/¯')
            else:
                if msg.get('reply_to_message'):
                    reply_id = msg['reply_to_message']['from']['id']
                    reply_name = msg['reply_to_message']['from']['first_name']
                elif len(msg['text'].split()) > 1:
                    u_id = msg['text'].split()[1]
                    try:
                        get = await bot.getChat(u_id)
                        reply_id = get['id']
                        reply_name = get['first_name']
                    except (TelegramError, KeyError):
                        await bot.sendMessage(msg['chat']['id'],
                                              'Invalid or unknown ID. Use format: /kick ID of the user',
                                              reply_to_message_id=msg['message_id'])
                        return
                else:
                    reply_id = None

                adm = await is_admin(msg['chat']['id'], msg['from']['id'], reply_id)

                if adm['user']:
                    try:
                        int(reply_id)
                    except (TypeError, ValueError):
                        return await bot.sendMessage(msg['chat']['id'], 'Reply to someone s message or enter his ID',
                                                     reply_to_message_id=msg['message_id'])
                    if adm['bot']:
                        if adm['reply']:
                            await bot.sendMessage(msg['chat']['id'], 'This one is an admin.',
                                                  reply_to_message_id=msg['message_id'])
                        else:
                            await bot.unbanChatMember(msg['chat']['id'], reply_id)
                            await bot.sendMessage(msg['chat']['id'], f'{msg["from"]["first_name"]} kicked {reply_name}!',
                                                  reply_to_message_id=msg['message_id'])
                    else:
                        await bot.sendMessage(msg['chat']['id'], 'Hey, I am not an admin here.',
                                              reply_to_message_id=msg['message_id'])


        elif msg['text'].split()[0] == '/mute' or msg['text'].split()[0] == '!mute':
            if msg['chat']['type'] == 'private':
                await bot.sendMessage(msg['chat']['id'], 'This command works only in groups. ¯\\_(ツ)_/¯')
            else:
                if msg.get('reply_to_message'):
                    reply_id = msg['reply_to_message']['from']['id']
                    reply_name = msg['reply_to_message']['from']['first_name']
                elif len(msg['text'].split()) > 1:
                    u_id = msg['text'].split()[1]
                    try:
                        get = await bot.getChat(u_id)
                        reply_id = get['id']
                        reply_name = get['first_name']
                    except (TelegramError, KeyError):
                        await bot.sendMessage(msg['chat']['id'],
                                              'Invalid or unknown ID. Use format: /mute ID of the user',
                                              reply_to_message_id=msg['message_id'])
                        return
                else:
                    reply_id = None

                adm = await is_admin(msg['chat']['id'], msg['from']['id'], reply_id)

                if adm['user']:
                    try:
                        int(reply_id)
                    except (TypeError, ValueError):
                        return await bot.sendMessage(msg['chat']['id'], 'Reply to someone s message or enter his ID',
                                                     reply_to_message_id=msg['message_id'])
                    if adm['bot']:
                        if adm['reply']:
                            await bot.sendMessage(msg['chat']['id'], 'This one is an admin',
                                                  reply_to_message_id=msg['message_id'])
                        else:
                            await bot.restrictChatMember(msg['chat']['id'], reply_id)
                            await bot.sendMessage(msg['chat']['id'], f'{msg["from"]["first_name"]} restricted {reply_name}!',
                                                  reply_to_message_id=msg['message_id'])
                    else:
                        await bot.sendMessage(msg['chat']['id'], 'Hey, I am not an admin here',
                                              reply_to_message_id=msg['message_id'])


        elif msg['text'].split()[0] == '/unmute' or msg['text'].split()[0] == '!unmute':
            if msg['chat']['type'] == 'private':
                await bot.sendMessage(msg['chat']['id'], 'This command works only in groups. ¯\\_(ツ)_/¯')
            else:
                if msg.get('reply_to_message'):
                    reply_id = msg['reply_to_message']['from']['id']
                    reply_name = msg['reply_to_message']['from']['first_name']
                elif len(msg['text'].split()) > 1:
                    u_id = msg['text'].split()[1]
                    try:
                        get = await bot.getChat(u_id)
                        reply_id = get['id']
                        reply_name = get['first_name']
                    except TelegramError:
                        await bot.sendMessage(msg['chat']['id'],
                                              'Invalid or unknown ID. Use format: /unmute ID of the user',
                                              reply_to_message_id=msg['message_id'])
                        return
                else:
                    reply_id = None

                adm = await is_admin(msg['chat']['id'], msg['from']['id'], reply_id)

                if adm['user']:
                    try:
                        int(reply_id)
                    except (TypeError, ValueError):
                        return await bot.sendMessage(msg['chat']['id'], 'Reply to someone s message or enter his ID',
                                                     reply_to_message_id=msg['message_id'])
                    if adm['bot']:
                        if adm['reply']:
                            await bot.sendMessage(msg['chat']['id'], 'This is an admin',
                                                  reply_to_message_id=msg['message_id'])
                        else:
                            await bot.restrictChatMember(msg['chat']['id'], reply_id,
                                                         can_send_messages=True,
                                                         can_send_media_messages=True,
                                                         can_send_other_messages=True,
                                                         can_add_web_page_previews=True)
                            await bot.sendMessage(msg['chat']['id'], '{} now you can talk here!'.format(reply_name),
                                                  reply_to_message_id=msg['message_id'])
                    else:
                        await bot.sendMessage(msg['chat']['id'], 'Hey, I am not an admin here.',
                                              reply_to_message_id=msg['message_id'])


        elif msg['text'].split()[0] == '/unban' or msg['text'].split()[0] == '!unban':
            if msg['chat']['type'] == 'private':
                await bot.sendMessage(msg['chat']['id'], 'This command works only in groups. ¯\\_(ツ)_/¯')
            else:
                if msg.get('reply_to_message'):
                    reply_id = msg['reply_to_message']['from']['id']
                    reply_name = msg['reply_to_message']['from']['first_name']
                elif len(msg['text'].split()) > 1:
                    u_id = msg['text'].split()[1]
                    try:
                        get = await bot.getChat(u_id)
                        reply_id = get['id']
                        reply_name = get['first_name']
                    except TelegramError:
                        await bot.sendMessage(msg['chat']['id'],
                                              'Invalid or unknown ID. Use the format: /unban ID of Users',
                                              reply_to_message_id=msg['message_id'])
                        return
                else:
                    reply_id = None

                adm = await is_admin(msg['chat']['id'], msg['from']['id'], reply_id)

                if adm['user']:
                    try:
                        int(reply_id)
                    except (TypeError, ValueError):
                        return await bot.sendMessage(msg['chat']['id'], 'Reply to someone s message or give his ID',
                                                     reply_to_message_id=msg['message_id'])
                    if adm['bot']:
                        if adm['reply']:
                            await bot.sendMessage(msg['chat']['id'], 'This is an admin',
                                                  reply_to_message_id=msg['message_id'])
                        else:
                            await bot.unbanChatMember(msg['chat']['id'], reply_id)
                            await bot.sendMessage(msg['chat']['id'], '{} unbanned {}!'.format(
                                      msg['from']['first_name'],
                                      reply_name),
                                                  reply_to_message_id=msg['message_id'])
                    else:
                        await bot.sendMessage(msg['chat']['id'], 'Hey, I am not an admin here.',
                                              reply_to_message_id=msg['message_id'])


        elif msg['text'].split()[0] == '/pin' or msg['text'].split()[0] == '!pin':
            if msg['chat']['type'] == 'private':
                await bot.sendMessage(msg['chat']['id'], 'This command works only in groups ¯\\_(ツ)_/¯')
            elif (await is_admin(msg['chat']['id'], msg['from']['id']))['user']:
                if msg.get('reply_to_message'):
                    await bot.pinChatMessage(msg['chat']['id'], msg['reply_to_message']['message_id'])
                else:
                    await bot.sendMessage(msg['chat']['id'], 'Please reply to some message to pin that message.',
                                          reply_to_message_id=msg['message_id'])


        elif msg['text'].split()[0] == '/unpin' or msg['text'].split()[0] == '!unpin':
            if msg['chat']['type'] == 'private':
                await bot.sendMessage(msg['chat']['id'], 'This command works only in groups. ¯\\_(ツ)_/¯')
            elif (await is_admin(msg['chat']['id'], msg['from']['id']))['user']:
                await bot.unpinChatMessage(msg['chat']['id'])
                await bot.sendMessage(msg['chat']['id'], 'The message is unpinned',
                                      reply_to_message_id=msg['message_id'])


        elif msg['text'].startswith('/title') or msg['text'].startswith('!title'):
            text = msg['text'][7:]
            if msg['chat']['type'] == 'private':
                await bot.sendMessage(msg['chat']['id'], 'This command works only in groups. ¯\\_(ツ)_/¯')
            elif (await is_admin(msg['chat']['id'], msg['from']['id']))['user']:
                if text == '':
                    await bot.sendMessage(msg['chat']['id'], 'Use format: /title title for the group',
                                          reply_to_message_id=msg['message_id'])
                else:
                    try:
                        await bot.setChatTitle(msg['chat']['id'], text)
                        await bot.sendMessage(msg['chat']['id'], 'New title for the group is successfully set!',
                                              reply_to_message_id=msg['message_id'])
                    except NotEnoughRightsError:
                        await bot.sendMessage(msg['chat']['id'],
                                              'I dont have the permission to change the group information',
                                              reply_to_message_id=msg['message_id'])
                    except TelegramError:
                        await bot.sendMessage(msg['chat']['id'], 'An error occurred.',
                                              reply_to_message_id=msg['message_id'])


        elif msg['text'] == '/config':
            if msg['chat']['type'] == 'private':
                await bot.sendMessage(msg['chat']['id'], 'This command works only in groups ¯\\_(ツ)_/¯')
            else:
                if (await is_admin(msg['chat']['id'], msg['from']['id']))['user']:
                    kb = InlineKeyboardMarkup(inline_keyboard=[
                        [dict(text='⚙️ Options for chat', callback_data='options {}'.format(msg['chat']['id']))],
                        [dict(text='🗑 Delete message', callback_data='del_msg')]
                    ])
                    await bot.sendMessage(msg['from']['id'], 'Configuration menu of the chat {}'.format(msg['chat']['title']),
                                          reply_markup=kb)
                    await bot.sendMessage(msg['chat']['id'], 'I have sent a configuration menu to your PM.',
                                          reply_to_message_id=msg['message_id'])
            return True

        elif msg['text'] == '/admdebug':
            res = await is_admin(msg['chat']['id'], msg['from']['id'],
                                 msg['reply_to_message']['from']['id'] if msg.get('reply_to_message') else None)
            await bot.sendMessage(msg['chat']['id'], res)
            return True

    elif msg.get('data'):

        if msg['data'].startswith('options'):
            await bot.answerCallbackQuery(msg['id'], 'Opening...')
            if (await is_admin(msg['data'].split()[1], msg['from']['id']))['user']:
                info = await bot.getChat(msg['data'].split()[1])
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [dict(text='IA', callback_data='ai')] +
                    [dict(text='None', callback_data='ai_switch {}'.format(msg['data'].split()[1]))],
                    [dict(text='🔙 Back', callback_data='back {}'.format(msg['data'].split()[1]))]
                ])
                await bot.editMessageText((msg['from']['id'], msg['message']['message_id']),
                                    'Chat  Options {}'.format(info['title']),
                                    reply_markup=kb)

        elif msg['data'].startswith('back'):
            info = await bot.getChat(msg['data'].split()[1])
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [dict(text='⚙️ Options for chat', callback_data='options {}'.format(msg['data'].split()[1]))],
                [dict(text='🗑 Delete Message', callback_data='del_msg')]
            ])
            await bot.editMessageText((msg['from']['id'], msg['message']['message_id']),
                                      'Configuration Menu of the chat {}'.format(info['title']),
                                      reply_markup=kb)

        elif msg['data'] == 'del_msg':
            await bot.deleteMessage((msg['from']['id'], msg['message']['message_id']))
