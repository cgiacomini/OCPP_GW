import logging
import asyncio

def before_all(context):
    # Access SERVER_URL from behave.ini
    context.server_url = context.config.userdata.get("SERVER_URL", "ws://localhost:9000")
    context.meter_stat_filename = context.config.userdata.get("METER_STAT_FILENAME", "meter_stat.json")

    # Configure logging
    logging.basicConfig(
        filename='charging_station.log',  # Log file name
        level=logging.DEBUG,              # Log level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    logger = logging.getLogger(__name__)
    
    logger.info('Logging setup complete.')
