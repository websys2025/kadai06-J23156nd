import requests
import json
import pandas as pd 


# --- APIリクエスト設定 ---
# アプリケーションID (このまま使用してください)
APP_ID = "b046a1f817b03c4112781933f6db9573b2a1feab"

# 取得する統計データのID (出入国管理統計 / 国籍・地域別 港別 入国外国人)
# 統計表ID: 0003288044
# 参考URL: https://www.e-stat.go.jp/stat-search/database?layout=dataset&toukei=00250011&statdisp_id=0003288044
STATS_DATA_ID = "0003288044"

# APIのベースURL
BASE_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

# パラメータ設定
params = {
    "appId": APP_ID,
    "statsDataId": STATS_DATA_ID,
    # "cdArea": "12101,12102,12103,12104,12105,12106", # この統計表では地域コードが「港」を表すため、今回はコメントアウトします
    # "cdCat01": "A1101", # この統計表では「国籍・地域」のコードを表すため、特定の国に絞り込みます
    
    "metaGetFlg": "Y",     # メタ情報（統計表名、項目名など）も取得
    "cntGetFlg": "N",      # カテゴリ情報は取得しない（データ本体メイン）
    "explanationGetFlg":"Y", # 説明情報も取得
    "annotationGetFlg":"Y", # 注釈情報も取得
    "sectionHeaderFlg":"1", # ヘッダー情報を付与
    "replaceSpChars":"0",   # 特殊文字を置換しない
    "lang": "J",           # 言語設定: 日本語

    # --- 変更点: 特定の国・地域（国籍）に絞り込み ---
    # cdCat01 はこの統計表では「国籍・地域」を表します。
    # 各国の正確なコードは、eStatの統計表詳細ページで確認できます。
    # ここでは、中国、ベトナム、モンゴルのコードを指定します。
    #   中国: 50140
   
    "cdCat01": "50140,
}

print("eStat-APIからデータを取得中...")
try:
    # APIリクエストを送信
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # HTTPエラー（4xx, 5xx）があれば例外を発生

    # レスポンスをJSON形式で解析
    data = response.json()

    # 取得したデータをPandas DataFrameで処理
    if data and "GET_STATS_DATA" in data and "STATISTICAL_DATA" in data["GET_STATS_DATA"]:
        statistical_data = data["GET_STATS_DATA"]["STATISTICAL_DATA"]

        # 統計表情報の表示
        if "TABLE_INF" in statistical_data:
            table_info = statistical_data["TABLE_INF"]
            print(f"\n--- 統計表情報 ---")
            print(f"統計表名: {table_info.get('STAT_NAME', 'N/A')} - {table_info.get('TITLE', 'N/A')}")
            print(f"最終更新日: {table_info.get('UPDATED_DATE', 'N/A')}")
            print("-" * 40)

        # 統計データからデータ部取得
        values = statistical_data.get('DATA_INF', {}).get('VALUE', [])
        if not values:
            print("データが見つかりませんでした。")
        else:
            # JSONからDataFrameを作成
            df = pd.DataFrame(values)

            # メタ情報取得 (CLASS_INF からカテゴリのIDと名称の対応を取得)
            meta_info = statistical_data.get('CLASS_INF', {}).get('CLASS_OBJ', [])

            # 統計データのカテゴリ要素をID(数字の羅列)から、意味のある名称に変更する
            for class_obj in meta_info:
                column_name = '@' + class_obj['@id']

                id_to_name_dict = {}
                if isinstance(class_obj['CLASS'], list):
                    for obj in class_obj['CLASS']:
                        id_to_name_dict[obj['@code']] = obj['@name']
                elif isinstance(class_obj['CLASS'], dict):
                    id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']
                
                if column_name in df.columns:
                    df[column_name] = df[column_name].replace(id_to_name_dict)

            # 統計データの列名を変換するためのディクショナリを作成
            col_replace_dict = {'@unit': '単位', '$': '値'}
            for class_obj in meta_info:
                org_col = '@' + class_obj['@id']
                new_col = class_obj['@name']
                col_replace_dict[org_col] = new_col

            new_columns = []
            for col in df.columns:
                if col in col_replace_dict:
                    new_columns.append(col_replace_dict[col])
                else:
                    new_columns.append(col)
            
            df.columns = new_columns
            
            print("\n--- 取得データ (Pandas DataFrame) ---")
            print(df.head(10)) # 最初の10行を表示して、絞り込み結果を確認しやすくする
            if len(df) > 10:
                print(f"\n... (全 {len(df)} 件中、最初の10件を表示しています)")

    elif "ERROR_INFO" in data:
        error_info = data["ERROR_INFO"]
        print(f"\nAPIエラーが発生しました:")
        print(f"  エラーコード: {error_info.get('ERROR_CODE')}")
        print(f"  エラーメッセージ: {error_info.get('ERROR_MSG')}")
        if error_info.get('REFERRER'):
            print(f"  参考情報: {error_info.get('REFERRER')}")
    else:
        print("\n予期せぬAPIレスポンス形式です。")

except requests.exceptions.RequestException as e:
    print(f"\nHTTPリクエストエラーが発生しました: {e}")
except json.JSONDecodeError:
    print("\nAPIレスポンスのJSON解析に失敗しました。")
except Exception as e:
    print(f"\n予期せぬエラーが発生しました: {e}")

print("\nプログラム終了。")
