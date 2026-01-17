import requests

# ----- Setting ----- #
scale_dict = {
    10: '1',
    20: '2',
    30: '3',
    40: '4',
    45: '5弱', 50: '5強',
    55: '6弱', 60: '6強',
    70: '7'
}
# -------------------- #

class EEW():
    def __init__(self, api):
        self.api = api


    def Get(self):
        try:
            req = requests.get(self.api)
            req.raise_for_status()

            if req.status_code != 200:
                return False, f"HTTPエラー: {req.status_code}"
            data = req.json()
            
            latest_eq = data[0]
            eq_id     = latest_eq['id']
            hypo_name = latest_eq['earthquake']['hypocenter']['name']
            magnitude = latest_eq['earthquake']['hypocenter']['magnitude']
            eq_time   = latest_eq['earthquake']['time']
            max_scale = scale_dict.get(latest_eq['earthquake']['maxScale'], '不明')
            message   = f"< 地震情報 >\n\n>> 震源地\n-{hypo_name}\n\n"
            message  += f">> マグニチュード\n-M{magnitude}\n\n"
            message  += f">> 最大震度\n-{max_scale}\n\n"
            message  += f">> 発生時刻\n-{eq_time}"

            return True, message, eq_id
        except requests.exceptions.RequestException as e:
            # リクエストが失敗したとき
            return False, f"地震データの取得中にエラーが発生しました: {e}"
        except Exception as e:
            # それ以外のエラー
            return False, f"地震データの取得中にエラーが発生しました: {e}"

        return None, None
