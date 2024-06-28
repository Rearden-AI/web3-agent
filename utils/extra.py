import requests
import os


def check_transactions_status():
    response = requests.post(url="https://defi.zpoken.dev/api/v1/transactions/check")
    if response.status_code == 200:
        return {"ok": True}
    else:
        return {"ok": False}

