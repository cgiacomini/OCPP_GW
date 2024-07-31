import logging
import json
import os
from behave import given, when, then

logger = logging.getLogger(__name__)

@given(u'the Charging Station with unique_id {unique_id} has connectors with initial statuses')
def step_impl(context, unique_id):
    pass
    #logger.debug(context)
    #for row in context.table:
        #logger.info(f"status:")
        #logger.info(f"status {row['connector_1']} {row['connector_2']}")
