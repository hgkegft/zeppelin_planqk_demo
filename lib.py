import json
import os

from loguru import logger
from planqk.service.client import PlanqkServiceClient

consumer_key = os.getenv("CONSUMER_KEY", None)
consumer_secret = os.getenv("CONSUMER_SECRET", None)
service_endpoint = os.getenv("SERVICE_ENDPOINT", None)


def estimate(series, cr, location, working_hours, year):
    logger.info("Start estimate...")

    data_ref = {"dataPoolId": "95b5dd46-8188-4e3b-8fa3-cc6e2289d596",
                "dataSourceDescriptorId": "3c1ed72a-a22f-4d93-9a69-32e6879c6dfc",
                "fileId": "e2215756-711d-4b47-9012-af581bb57d7f"}

    params = dict()
    params["X_test"] = [[series, cr, location, working_hours, year]]

    try:
        result = execute_on_planqk(data_ref=data_ref, params=params)
        if result["result"] is None:
            msg = "Timeout: No valid result could be calculated in the given time."
        else:
            msg = result["result"]
        logger.info(msg)
    except Exception as e:
        msg = str(e)
        logger.error(msg)

    return msg


def execute_on_planqk(data_ref=None, params=None):
    logger.info(params)

    client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)
    logger.info("Starting execution of the service...")

    job = client.start_execution(data_ref=data_ref, params=params)

    MAX_TIME = 600
    timeout = 25
    sleep = 5
    count = 0
    while True:
        try:
            count += 1
            client.wait_for_final_state(job.id, timeout=timeout, wait=sleep)
            logger.info(f"{count:03d} | ...Found result!")
            result = client.get_result(job.id)
            break
        except Exception as e:
            logger.info(f"{e}")
            if count >= int(MAX_TIME / timeout):
                logger.info(f"{count:03d} | ...Found no result...stop.")
                result = {"result": None}
                break
    return result
