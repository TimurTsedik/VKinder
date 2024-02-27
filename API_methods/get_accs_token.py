from urllib.parse import urlencode

def get_token():
    """
    Функция для получения токена
    Одноразовая авторизация
    :return:
    """

    app_id = "51865387"
    oath_url = "https://oauth.vk.com/authorize"
    params = {
        "client_id": app_id,
        "redirect_uri": "https://oauth.vk.com/blank.html",
        "display": "page",
        "scope": "friends,photos,offline, status",
        "response_type": "token"
    }
    oauth_url = f"{oath_url}?{urlencode(params)}"
    print(oauth_url)

get_token()