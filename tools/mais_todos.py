from typing import Optional

from requests import Response, post

from app.models import LogApi


def send_cashback(cashback_value: float, document: str) -> dict:
    payload = {"document": document, "cashback": cashback_value}
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
            app="MaisTodosAPI",
            status_code=response.status_code,
        )
    else:
        response_data["error_message"] = "Error sending cashback to MaisTodos API"

    # response_data = {
    #     "createdAt": "2022-12-22T15:33:05.244Z",
    #     "message": "Cashback criado com sucesso!",
    #     "id": "1",
    #     "document": "33535353535",
    #     "cashback": "10",
    # }
    return response_data
