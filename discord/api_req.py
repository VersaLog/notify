import requests

def get_weather(location: str, api_key: str):
    api = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": api_key,
        "units": "metric",
        "lang": "ja"
    }

    try:
        req = requests.get(api, params=params, timeout=10)

        if req.status_code != 200:
            return False, f"HTTPエラー: {req.status_code}"

        data = req.json()

        msg = (
            f"< {data['name']}の天気予報 >\n\n"
            f"> 天気\n・{data['weather'][0]['description']}\n\n"
            f"> 気温\n・{data['main']['temp']}°C\n\n"
            f"> 湿度\n・{data['main']['humidity']}%\n\n"
            f"> 気圧\n・{data['main']['pressure']} hPa\n\n"
            f"> 風速\n・{data['wind']['speed']} m/s"
        )

        return True, msg

    except requests.exceptions.RequestException as e:
        return False, f"リクエスト例外: {e}"
