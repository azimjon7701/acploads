import requests


def get_fmcsa_data(query_param: str, query_string: str) -> dict:
    url = 'https://places.anycappro.com/fmcsa'
    params = {'query_param': query_param, 'query_string': query_string}
    headers = {'accept': 'application/json'}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        # Agar so'rov muvaffaqiyatli bo'lsa, javobni JSON formatida qaytarib beramiz
        return response.json()
    else:
        # Agar muvaffaqiyatsiz bo'lsa, status kodi va tekshirilgan xabar
        return {
            'error': 'error'
        }
