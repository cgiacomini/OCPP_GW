import asyncio
from behave import when

@when('the Charge Station send meter statistics to the server')
def send_meter_statistics(context):
    data_file_path = context.config.userdata['meter_data_file']
    charge_point = ChargePoint(context.config.userdata['charge_point_id'])
    charge_point.send_meter_values(data_file_path)

@when('the Charge Station send meter statistics to the server')
def step_impl(context, interval):
    """Start sending meter statistics to the server."""
    async def send_meter_statistics(cp_info):
        cp_info["charge_point"].meters_task = context.loop.create_task(cp_info["charge_point"].meters_task())
        await asyncio.sleep(int(interval))
        await cp_info["charge_point"].stop()

    for cp_info in context.charge_points:
        context.loop.run_until_complete(send_meter_statistics(cp_info))
        
        
import json
import os
import asyncio
from behave import when, then
from tests.features.utils.charge_point import ChargePoint

@when('I send meter statistics to the server')
def send_meter_statistics(context):
    data_file_path = context.config.userdata['meter_data_file']
    interval = int(context.config.userdata.get('meter_value_interval', 60))
    charge_point = ChargePoint(context.config.userdata['charge_point_id'])
    asyncio.run(charge_point.send_meter_values(data_file_path, interval))
