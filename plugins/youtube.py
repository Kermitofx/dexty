#@Anandpskerala
import json
import math
import os
import requests
import subprocess
import time

from config import Config


import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
