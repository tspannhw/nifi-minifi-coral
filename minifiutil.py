import argparse
from PIL import Image
import glob
import time
import argparse
import os.path
import re
import sys
import tarfile
import os
import datetime
import math
import random, string
import base64
import json
from time import sleep
from time import gmtime, strftime
import datetime
import subprocess
import os
import base64
import uuid
import datetime
import traceback
import math
import random, string
import socket
import base64
import json
import math
import psutil
import socket

#### - Standard Utilities for MiNiFi and IoT Projects
#### - Timothy Spann

def randomword(length):
  return ''.join(random.choice(string.lowercase) for i in range(length))


def IP_address():
    try:
      external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
      socket_family = socket.AF_INET
      s = socket.socket(socket_family, socket.SOCK_DGRAM)
      s.connect(external_IP_and_port)
      answer = s.getsockname()
      s.close()
      return answer[0] if answer else None
    except socket.error:
      return None

def getCPUtemperature():
  res = os.popen('vcgencmd measure_temp').readline()
  return (res.replace("temp=", "").replace("'C\n", ""))

