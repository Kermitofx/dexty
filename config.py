import amanobot
import amanobot.aio
import asyncio


token = "739443555:AAH1fNTnVfOIieCIx_Z-LyewYVn68D9MmTk"


loop = asyncio.get_event_loop()  # Do not change this


bot = amanobot.aio.Bot(token)
na_bot = amanobot.Bot(token)


me = loop.run_until_complete(bot.getMe())
bot_username = me['username']
bot_id = me['id']


keys = dict(
    here = {'app_id': 'QGFyjwIngwdd0psY2jI4', 'app_code': 'L29BFJLe3H1B_Am8qJuwpw'},  #You can get a key at https://here.com
    yandex = 'trnsl.1.1.20190911T054155Z.092711bf269c8432.c033eeec0e160b66727a6bc750f2b50128439550',                                            #You can get a key at https://tech.yandex.com/translate
    giphy = 'ji9MD6TT6fxnUF0h4NHnsXSVMvfH69ZT',                                             #You can get a key at https://developers.giphy.com
)

git_repo = ('https://github.com/Anandpskerala/EduuRobot', 'unstable') #Repository where your bot is in

max_time = 60

version = open('version.txt').read()

logs = 646146866

backups_chat = 646146866  # Put a 0, False or None to disable.
backup_hours = ['00:00', '12:00']

sudoers = [
    646146866
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
