import os

from loguru import logger
from planqk.service.client import PlanqkServiceClient

consumer_key = os.getenv("CONSUMER_KEY", None)
consumer_secret = os.getenv("CONSUMER_SECRET", None)
service_endpoint = os.getenv("SERVICE_ENDPOINT", None)
model_as_string_base64 = os.getenv("MODEL_AS_STRING_BASE64", None)


def estimate(series, location, working_hours, year):

    data = dict()
    data["X_test"] = [[series, location, working_hours, year]]

    params = dict()
    params["mode"] = "predict"
    params["model_as_string_base64"] = model_as_string_base64

    result = execute_on_planqk(data, params)
    if result["result"] is None:
        msg = "Timeout: No valid result could be calculated in the given time."
    else:
        msg = result["result"]
    return msg


def execute_on_planqk(data=None, params=None):
    logger.info(params)

    client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)
    logger.info("Starting execution of the service...")

    job = client.start_execution(data=data, params=params)

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
