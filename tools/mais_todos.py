from typing import Optional

from requests import Response, post

from app.models import LogApi, User
from tools.person_docs_helper import remove_mask_cpf


def send_cashback(cashback_value: float, document: str, current_user: User) -> dict:
    payload = {"document": remove_mask_cpf(document), "cashback": cashback_value}
    url = "https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback"
    headers: dict = {
        "Content-Type": "application/json;charset=UTF-8",
    }
    try:
        response: Optional[Response] = post(url=url, json=payload, headers=headers)
    except Exception:
        # TODO Save the error when creating the log saving mechanism
        response: Optional[Response] = None

    response_data: dict = {}
    if response is not None:
        if response.status_code == 200:
            response_data: dict = response.json()
        else:
            response_data["error_message"] = str(response.text).replace('"', "")

        # Save log API
        LogApi.save_log(
            _request=response.request,
            response_json=response_data,
            user=current_user,
            status_code=response.status_code,
        )
    else:
        response_data["error_message"] = "Error sending cashback to MaisTodos API"
    return response_data
