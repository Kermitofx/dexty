import amanobot
import amanobot.aio
import asyncio
import os


token = os.environ.get("TokenBot", "")


loop = asyncio.get_event_loop()  # Do not change this


bot = amanobot.aio.Bot(token)
na_bot = amanobot.Bot(token)


me = loop.run_until_complete(bot.getMe())
bot_username = me['username']
bot_id = me['id']


keys = dict(
    here = {'app_id': os.environ.get("appid", ""), 'app_code': os.environ.get("appcode", "")},  #You can get a key at https://here.com
    yandex = os.environ.get("yandex", ""),                                            #You can get a key at https://tech.yandex.com/translate
    giphy = os.environ.get("giphy", ""),                                             #You can get a key at https://developers.giphy.com
)

git_repo = ('https://github.com/Anandpskerala/EduuRobot', 'unstable') #Repository where your bot is in

max_time = 60

version = open('version.txt').read()

logs = -1001296501406

backups_chat = -1001254736531  # Put a 0, False or None to disable.
backup_hours = ['05:00', '15:50']

sudoers = [
    646146866,658571574
]

enabled_plugins = [
    'processmsg',
    'start',
    'rules',
    'shorten',
    'sed',
    'kibe',
    'translate',
    'rextester',
    'inlines',
    'welcome',
    'admins',
    'warns',
    'prints',
    'pypi',
    'weather',
    'youtube',
    'ping',
    'gif',
    'git',
    'reddit',
    'coub',
    'sudos',
    'ids',
    'ip',
    'jsondump',
    'dice',
    'misc',
    'antipedro'
]
