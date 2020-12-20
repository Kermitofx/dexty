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

import html
import re
from uuid import uuid4

import duckpy.aio
import aiohttp
from amanobot.exception import TelegramError
from urllib.parse import quote_plus
from amanobot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

from config import bot, bot_username
from .youtube import search_yt


geo_ip = 'http://ip-api.com/json/'
googl_img_api = 'https://apikuu.herokuapp.com/api/v0/sakty/imej'

ddg_client = duckpy.aio.Client()


def escape_definition(prox):
    for key, value in prox.items():
        if isinstance(value, str):
            prox[key] = html.escape(value)
    return prox


async def inlines(msg):
    if 'query' in msg:
        first_name = msg['from']['first_name']
        user_id = msg['from']['id']
        if 'username' in msg['from']:
            username = '@' + msg['from']['username']
        else:
            username = 'nenhum'
        msg["query"] = msg["query"] or "0"
        if msg['query'].split()[0].lower() == 'ip' and len(msg['query']) > 6:
            async with aiohttp.ClientSession() as session:
                r = await session.get(geo_ip + msg['query'][3:])
                rjson = await r.json()
            res = "\n".join(["*{}*: `{}`".format(i, rjson[i]) for i in rjson])

            articles = [InlineQueryResultArticle(
                id='a', title='Information from ' + msg['query'][3:], input_message_content=InputTextMessageContent(
                    message_text='*Query*: `' + msg['query'][3:] + '`\n\n' + res, parse_mode="Markdown"))]

            await bot.answerInlineQuery(msg['id'], results=articles, cache_time=60, is_personal=True)


        elif msg['query'].split()[0].lower() == 'echo' and len(msg['query'].split()) >= 2:
            articles = [InlineQueryResultArticle(
                id='a', title=msg['query'][5:],
                input_message_content=InputTextMessageContent(message_text=msg['query'][5:]))]

            await bot.answerInlineQuery(msg['id'], results=articles, cache_time=60, is_personal=True)


        elif msg['query'].split()[0].lower() == 'duck' and len(msg['query'].split()) >= 2:
            count = 50
            number = 1
            search = msg['query'][5:]
            duc = await ddg_client.search(str(search))
            articles = []
            if duc:
                if count + number > len(duc):
                    maxdef = len(duc)
                else:
                    maxdef = count + number
                for i in range(number - 1, maxdef - 1):
                    deftxt = duc[i]
                    deftxt = escape_definition(deftxt)
                    articles.append(InlineQueryResultArticle(
                        id=str(uuid4()),
                        title=deftxt['title'],
                        thumb_url='https://piics.ml/i/002.png',
                        description=deftxt['url'],
                        input_message_content=InputTextMessageContent(
                            message_text=f"<b>{deftxt['title']}</b>\n{deftxt['url']}",
                            parse_mode='HTML')))
            else:
                articles.append(InlineQueryResultArticle(
                    id=str(uuid4()),
                    title="No results.",
                    input_message_content=InputTextMessageContent(
                        message_text=f"Sem resultados para '{search}'."
                    )))

            await bot.answerInlineQuery(msg['id'], results=articles, cache_time=60, is_personal=True)


        elif msg['query'].split()[0].lower() == 'img':
            query = msg['query'][4:]
            async with aiohttp.ClientSession() as session:
                r = await session.get(googl_img_api, params=dict(cari=query))
                img = await r.json()
            resp = []
            for k, result in enumerate(img):
                if k == 50:
                    break
                resp.append(InlineQueryResultPhoto(
                    id=str(uuid4()),
                    photo_url=result["Isi"],
                    thumb_url=result["Tumbnil"],
                    caption=html.unescape(result["Deskripsi"])
                ))
            await bot.answerInlineQuery(msg['id'], results=resp, cache_time=60, is_personal=True)


        elif msg['query'].split()[0].lower() == 'invert' and len(msg['query'].split()) >= 2:
            query = msg['query'][7:]
            articles = [InlineQueryResultArticle(id='abcde', title=query[::-1],
                                                 input_message_content=InputTextMessageContent(
                                                     message_text=query[::-1]))]

            await bot.answerInlineQuery(msg['id'], results=articles)


        elif msg['query'].split()[0].lower() == 'markdown' and len(msg['query'].split()) >= 2:
            articles = [InlineQueryResultArticle(
                id='a', title=msg['query'][9:],
                input_message_content=InputTextMessageContent(message_text=msg['query'][9:], parse_mode='Markdown'))]

            await bot.answerInlineQuery(msg['id'], results=articles)


        elif msg['query'].split()[0].lower() == 'html' and len(msg['query'].split()) >= 2:
            articles = [InlineQueryResultArticle(
                id='a', title=msg['query'][5:],
                input_message_content=InputTextMessageContent(message_text=msg['query'][5:], parse_mode='html'))]
            try:
                await bot.answerInlineQuery(msg['id'], results=articles)
            except TelegramError:
                articles = [InlineQueryResultArticle(
                    id='a', title='Text with formatting errors.', input_message_content=InputTextMessageContent(
                        message_text='An error has occurred. probably because you used an unsupported tag, or because you forgot to close any tags. Supported tags are these: <b>, <i>, <code>, <a> e <pre>.'))]
                await bot.answerInlineQuery(msg['id'], results=articles)


        elif msg['query'].split()[0].lower() == 'yt' and len(msg['query'].split()) >= 2:
            articles = []
            search = await search_yt(msg['query'][3:])
            for i in search:
                articles.append(InlineQueryResultArticle(
                    id=str(uuid4()), title=i['title'],
                    thumb_url=f"https://i.ytimg.com/vi/{i['url'].split('v=')[1]}/default.jpg",
                    input_message_content=InputTextMessageContent(message_text=i['url'])))
            if not articles:
                articles.append(InlineQueryResultArticle(
                    id=str(uuid4()), title=f'Nenhum resultado encontrado para "{msg["query"][3:]}".',
                    input_message_content=InputTextMessageContent(message_text='.')))

            await bot.answerInlineQuery(msg['id'], results=articles, cache_time=60, is_personal=True)


        elif msg['query'].split()[0].lower() == 'print' and len(msg['query'].split()) >= 2:
            url = msg['query'][6:]
            if re.match(r'^https?://', msg['query'][6:]):
                url = msg['query'][6:]
            else:
                url = 'http://' + msg['query'][6:]
            quoted_url = "http://api.olixao.ml/print?q=" + quote_plus(url)
            try:
                res = [InlineQueryResultPhoto(
                    id='a',
                    photo_url=quoted_url,
                    thumb_url=quoted_url,
                    caption=url
                )]
                await bot.answerInlineQuery(msg['id'], results=res, cache_time=60, is_personal=True)
            except Exception as e:
                res = [InlineQueryResultArticle(
                    id='a', title='Error',
                    input_message_content=InputTextMessageContent(str(e)))]
                await bot.answerInlineQuery(msg['id'], results=res, cache_time=60, is_personal=True)


        elif msg['query'].lower() == 'faces' or msg['query'].lower() == 'f':
            faces = ['¯\\_(ツ)_/¯', '( ͡° ͜ʖ ͡°)', '( ͡~ ͜ʖ ͡°)', '( ͡◐ ͜ʖ ͡◑))', '( ͡◔ ͜ʖ ͡◔)', '( ͡⚆ ͜ʖ ͡⚆)',
                     '( ͡ʘ ͜ʖ ͡ʘ)', 'ヽ༼ຈل͜ຈ༽ﾉ', '༼ʘ̚ل͜ʘ̚༽', '(╯°□°）╯', '(ﾉ◕ヮ◕)ﾉ', '(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧', '(◕‿◕)', '(｡◕‿‿◕｡)',
                     '(っ◕‿◕)っ', '(づ｡◕‿‿◕｡)づ', '༼ つ ◕_◕ ༽つ', '(ง ͠° ͟ل͜ ͡°)ง', '(ง\'̀-\'́)ง', 'ᕙ(⇀‸↼‶)ᕗ', '(҂⌣̀_⌣́)',
                     'ᕦ(ò_óˇ)ᕤ', '╚(ಠ_ಠ)=┐', 'ლ(ಠ益ಠლ)', '\\_(ʘ_ʘ)_/', '( ⚆ _ ⚆ )', '(ಥ﹏ಥ)', '﴾͡๏̯͡๏﴿', '(◔̯◔)', '(ಠ_ಠ)',
                     '(ಠ‿ಠ)', '(¬_¬)', '(¬‿¬)', '\\ (•◡•) /', '(◕‿◕✿)', '( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)']
            articles = [
                InlineQueryResultArticle(id=str(uuid4()), title=face, input_message_content=dict(message_text=face)) for
                face in faces]

            await bot.answerInlineQuery(msg['id'], results=articles)


        elif msg['query'].split()[0].lower() == 'hidemsg':
            articles = [InlineQueryResultArticle(
                id='a', title='Resultado: ' + msg['query'][8:],
                input_message_content=InputTextMessageContent(message_text='\u2060' * 3600 + msg['query'][8:]))]
            await bot.answerInlineQuery(msg['id'], results=articles, cache_time=60, is_personal=True)

        else:
            articles = [
                InlineQueryResultArticle(
                    id='a', title='Informations', thumb_url='https://piics.ml/amn/eduu/info.png',
                    description='Displays information about you',
                    input_message_content=dict(
                        message_text='<b>Your information:</b>\n\n<b>Name:</b> <code>' + html.escape(
                            first_name) + '</code>\n<b>ID:</b> <code>' + str(
                            user_id) + '</code>\n<b>Username:</b> <code>' + username + '</code>', parse_mode="HTML"
                    )
                ),
                InlineQueryResultArticle(
                    id='b', title='Duck', thumb_url='https://piics.ml/amn/eduu/duck.png',
                    description='Search DuckDuckGo via inline.',
                    input_message_content=dict(
                        message_text='<b>Use:</b> <code>@{} duck</code> - Search DuckDuckGo via inline.'.format(
                            bot_username), parse_mode='HTML'
                    )
                ),
                InlineQueryResultArticle(
                    id='c', title='Faces (f)', thumb_url='https://piics.ml/amn/eduu/faces.png',
                    description='Shows a list of smiley faces ¯\\_(ツ)_/¯',
                    input_message_content=dict(
                        message_text='<b>Use:</b> <code>@{} faces</code> - Displays a list of smiley faces :D'.format(
                            bot_username), parse_mode='HTML'
                    )
                ),
                InlineQueryResultArticle(
                    id='d', title='Hidemsg', thumb_url='https://piics.ml/amn/eduu/hidemsg.png',
                    description='Hides a message that does not appear in recent actions when deleted within 1 minute.',
                    input_message_content=dict(
                        message_text='<b>Use:</b> <code>@{} hidemsg</code> - To send a message that if you are off even 1 minute does not appear in the <i>recent developments</i>, a group.'.format(
                            bot_username), parse_mode='HTML'
                    )
                ),
                InlineQueryResultArticle(
                    id='f', title='img', thumb_url='https://piics.ml/amn/eduu/img.png',
                    description='Online image finder.',
                    input_message_content=dict(
                        message_text='<b>Use:</b> <code>@{} img</code> - Online image finder.'.format(
                            bot_username), parse_mode='HTML'
                    )
                ),
                InlineQueryResultArticle(
                    id='g', title='ip', thumb_url='https://piics.ml/amn/eduu/ip.png',
                    description='Displays information for a specific IP/URL.',
                    input_message_content=dict(
                        message_text='<b>Use:</b> <code>@{} ip</code> - Displays information of particular IP / URL.'.format(
                            bot_username), parse_mode='HTML'
                    )
                ),
                InlineQueryResultArticle(
                    id='h', title='print', thumb_url='https://piics.ml/amn/eduu/print.png',
                    description='Makes a screenshot of the page.',
                    input_message_content=dict(
                        message_text='<b>Use:</b> <code>@{} print</code> - Take a screenshot of a page.'.format(
                            bot_username), parse_mode='HTML'
                    )
                ),
                InlineQueryResultArticle(
                    id='i', title='run', thumb_url='https://piics.ml/amn/eduu/html.png',
                    description='Executes codes via inline.',
                    input_message_content=dict(
                        message_text='<b>Use:</b> <code>@{0} run &lt;lang&gt; &lt;code&gt;</code> - Executes codes via inline.\n\nEx.: <code>@{0} run python3 print("Hello to the world")</code>'.format(
                            bot_username), parse_mode='HTML'
                    )
                ),
                InlineQueryResultArticle(
                    id='j', title='yt', thumb_url='https://piics.ml/amn/eduu/yt.png',
                    description='Searches YouTube videos via inline.',
                    input_message_content=dict(
                        message_text='<b>Use:</b> <code>@{} yt</code> - Search YouTube videos via inline.'.format(
                            bot_username), parse_mode='HTML'
                    )
                )
            ]

            await bot.answerInlineQuery(msg['id'], results=articles, cache_time=60, is_personal=True)
