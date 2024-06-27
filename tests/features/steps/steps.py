import logging
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from steps.connection_steps import *
from steps.boot_notification_steps import *
from steps.response_steps import *
from steps.heartbeat_steps import *
from steps.close_connection_steps import *

logging.basicConfig(level=logging.DEBUG)
