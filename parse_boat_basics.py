import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import codecs
import string
import platform
import re
import time


def get_path(subfolder=''):
    c_os = platform.system()
    if c_os == "Windows":
        path_to_parse = os.getcwd() + '\\' + subfolder + '\\'
    else:
        path_to_parse = os.getcwd() + '/' + subfolder + '/'
    return path_to_parse


