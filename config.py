import os

TOKEN = os.environ.get("TokenBot", "")
API_HASH = os.environ.get("HASH", "")
APP_ID = os.environ.get("ID", "")

log_chat = -1001296501406

super_sudoers = [646146866]  # List of super sudoers (they can control what sudoers can do)
sudoers = [658571574]
sudoers += super_sudoers

prefix = ["/", "!"]  # Prefix used for user commands.

disabled_plugins = []  # List of plugins to not load.
