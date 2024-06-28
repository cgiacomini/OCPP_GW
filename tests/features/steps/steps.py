import logging
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from steps.boot_notification_request_steps import *
from steps.boot_notification_response_steps import *
from steps.heartbeat_request_steps import *
from steps.heartbeat_response_steps import *
from steps.open_connection_steps import *
from steps.close_connection_steps import *

logging.basicConfig(level=logging.DEBUG)

