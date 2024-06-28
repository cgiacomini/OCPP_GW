import logging
import asyncio

def before_all(context):
    # Access SERVER_URL from behave.ini
    context.server_url = context.config.userdata.get("SERVER_URL", "ws://localhost:9000")
