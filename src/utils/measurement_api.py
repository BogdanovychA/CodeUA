# -*- coding: utf-8 -*-

import logging

import httpx

from utils.secret import GA_ID, GA_SECRET_KEY

# DEBUG = True
DEBUG = False


logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


async def log_event(
    client_id: str, platform: str, event_name: str, page_path: str
) -> bool:
    """Логує подію"""

    suffix = "debug/" if DEBUG else ""
    url = (
        f"https://www.google-analytics.com/{suffix}mp/collect?"
        f"measurement_id={GA_ID}&api_secret={GA_SECRET_KEY}"
    )

    payload = {
        "client_id": client_id,
        "events": [
            {
                "name": event_name,
                "params": {
                    "page_path": page_path,
                    "platform": platform,
                },
            }
        ],
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=5.0)

            if DEBUG:
                if response.status_code != 200:
                    logger.warning(
                        f"GA debug unexpected status: {response.status_code}"
                    )
                    return False

                debug_result = response.json()

                validation_messages = debug_result.get('validationMessages', [])

                if validation_messages:
                    logger.warning(f"GA validation issues: {validation_messages}")
                    return False
                else:
                    logger.debug(f"GA event '{event_name}' validated successfully")
                    return True
            else:
                if response.status_code == 204:
                    # logger.info(f"GA event '{event_name}' sent successfully")
                    return True
                else:
                    logger.warning(
                        f"GA unexpected status {response.status_code} "
                        f"for event '{event_name}'"
                    )
                    return False

    except httpx.TimeoutException:
        logger.error("Analytics request timeout")
        return False

    except httpx.RequestError as e:
        logger.error(f"Analytics request failed: {e}")
        return False

    except Exception as e:
        logger.exception(f"Unexpected analytics error: {e}")
        return False
