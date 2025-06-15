import requests
import json

# --- オープンデータ取得プログラム kadai6-2.py ---
# このプログラムは、世界中のオープンデータの一つである「PokeAPI」から、
# ポケモンのデータを取得します。

# --- 参照するオープンデータの名前と概要 ---
# データ名: PokeAPI (ポケモンAPI)
# 概要: ポケモンのゲーム、アニメ、カードゲームなどに関する膨大なデータを無料で提供するオープンAPIです。
#       ポケモンごとの能力、タイプ、技、図鑑情報、進化の過程など、多岐にわたる情報が含まれています。
#       開発者やファンがポケモン関連のアプリケーションやツールを作成するのに広く利用されています。

# --- エンドポイントと機能 ---
# PokeAPIのベースURL: https://pokeapi.co/api/v2/
# 機能: 特定のポケモンIDや名前、能力、タイプなどの情報に対してHTTPリクエストを送信し、
#       その詳細なデータをJSON形式で取得します。
#       このプログラムでは、特定のポケモン（例: Ditto）の詳細情報を取得します。
# ドキュメント: https://pokeapi.co/docs/v2
# (APIの利用方法、各エンドポイントの詳細、レスポンスの構造について詳細を確認できます。)

# --- 使い方 ---
# 1. このプログラムを実行すると、指定されたポケモンのデータがPokeAPIから取得され、
#    JSON形式で整形されて表示されます。
# 2. 取得したいポケモンを変更するには、'POKEMON_NAME_OR_ID' の値を変更してください。
#    例: 'pikachu', 'charizard', '1', '25' など。

# --- APIリクエスト設定 ---
# 取得したいポケモンの名前またはIDを指定
POKEMON_NAME_OR_ID = "ditto" # あなたが提供したJSONに倣い「メタモン (Ditto)」を設定

# PokeAPIのポケモン詳細エンドポイント
BASE_URL = f"https://pokeapi.co/api/v2/pokemon/{POKEMON_NAME_OR_ID}/"

print(f"PokeAPIからポケモン '{POKEMON_NAME_OR_ID}' のデータを取得中...")

try:
    # APIリクエストを送信
    response = requests.get(BASE_URL)
    response.raise_for_status() # HTTPエラー（4xx, 5xx）があれば例外を発生

    # レスポンスをJSON形式で解析
    pokemon_data = response.json()

    # 取得したデータを整形して表示
    print("\n--- 取得データ ---")
    print(f"ポケモン名: {pokemon_data.get('name', 'N/A')}")
    print(f"ID: {pokemon_data.get('id', 'N/A')}")
    print(f"高さ: {pokemon_data.get('height', 'N/A')} (デシメートル)")
    print(f"重さ: {pokemon_data.get('weight', 'N/A')} (ヘクトグラム)")

    print("\n--- タイプ ---")
    if pokemon_data.get('types'):
        for poketype in pokemon_data['types']:
            print(f"  - {poketype['type']['name']}")
    else:
        print("  タイプ情報なし")

    print("\n--- 特性（アビリティ） ---")
    if pokemon_data.get('abilities'):
        for ability_info in pokemon_data['abilities']:
            hidden_status = "(隠れ特性)" if ability_info.get('is_hidden') else ""
            print(f"  - {ability_info['ability']['name']} {hidden_status}")
    else:
        print("  特性情報なし")

    print("\n--- 主要なステータス ---")
    if pokemon_data.get('stats'):
        for stat_info in pokemon_data['stats']:
            print(f"  - {stat_info['stat']['name']}: {stat_info['base_stat']}")
    else:
        print("  ステータス情報なし")

    print("\n--- 鳴き声URL ---")
    if pokemon_data.get('cries') and pokemon_data['cries'].get('latest'):
        print(f"  最新: {pokemon_data['cries']['latest']}")
    else:
        print("  鳴き声URLなし")
    
    print("\n--- 全体のJSONデータ（一部抜粋） ---")
    # より詳細なデータ構造を確認したい場合は、コメントを解除して全て表示できます。
    # print(json.dumps(pokemon_data, indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    # HTTPリクエスト自体でエラーが発生した場合（ネットワーク接続など）
    print(f"\nエラー: HTTPリクエスト中に問題が発生しました: {e}")
except json.JSONDecodeError:
    # APIレスポンスのJSON解析に失敗した場合
    print("\nエラー: APIレスポンスのJSON解析に失敗しました。レスポンスが不正な形式である可能性があります。")
except Exception as e:
    # その他の予期せぬエラー
    print(f"\n予期せぬエラーが発生しました: {e}")

print("\nプログラム終了。")
