
from openai import OpenAI
import os
from glob import glob

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# SYSTEM_PROMPT（行为规则 + 输出规范 + 示例）
SYSTEM_PROMPT = """
あなたはポーカートーナメント情報抽出および分析アシスタントです。  
タスクは2段階に分かれます：  
1. 入力される Markdown テキストからトーナメントの固定情報を抽出してください。  
2. 賞金・賞品データを分析し、要約結果を prizes_analyze フィールドに整理してください。  

⚠️ 注意事項：
- 出力は JSON のみ。余計な文字は不要。  
- 欠損フィールドは null。  
- 日付・時間 → "YYYY-MM-DD HH:MM"（24時間制）  
- 金額 → 整数のみ、単位なし  
- Coin 換算 → 1 Coin = 1円  
- チケット類は金額不明 → reward_value_jpy = null  
- 分析でチケット類は「0円」として集計すること  
- すべてのフィールドの文字列長は1000文字未満です。

---

抽出フィールド一覧：  

**基本情報（抽出そのまま）**  
- event_name: トーナメント名  
- event_link: トーナメントリンク（なければ null）  
- status: トーナメントの状態（例：待機中 / 開催中 / 終了）  
- shop_id: 店舗id, 店舗リンクの末尾数字部分  
- shop_name: 店舗名 
- official_page: 公式ページリンク  
- start_time: 開始日時  
- game_rule: ゲームルール（開始チップ、玩法、ブラインド構造など可能な限り詳細）  
- entry_fee: 参加費（円整数）  
- re_entry: 再入場ルール（例：5000円 / unlimited / no rebuy）  
- prizes: 賞金・賞品リスト（各要素：rank, reward_raw, reward_type, reward_value_jpy）  
- prizes_original: 原文の賞品情報テキスト  
- address: 開催場所住所
- prefecture: 都道府県（例：東京都）
- city_ward: 市区町村（例：新宿区）
- tel: 電話番号（なければ null）  

**分析情報（新規追加）**  
- prizes_analyze: 賞品データの要約と分析結果  
  - total_winners: 入賞人数（prizes 内の rank 数）  
  - total_value_jpy: 総賞金額（Coin 等を換算して合計、ticket/other換算不能は0円扱い）  
  - reward_categories: 出現した賞品タイプ一覧（例：["coin","ticket"]）  
  - rank_list: 順位ごとの報酬整理リスト（rank, reward_summary, reward_value_jpy）  
  - reward_summary: 簡潔な説明文（例：「35000円 + チケット1枚」）  

---

出力例：

{
  "event_name": "Holiday Big 5K",
  "event_link": "https://pokerguild.jp/tournaments/123",
  "status": "待機中",
  "shop_id": 264,
  "shop_name": "KK LIVE SHINJUKU",
  "official_page": "https://ggpokerlive.jp/shinjuku/",
  "start_time": "2025-08-16 11:30",
  "game_rule": "50,000点 / ノーリミット / テキサスホールデム / normal / Others",
  "entry_fee": 5000,
  "re_entry": "5000円 / マルチリエントリー",
  "prizes": [
    {"rank":"1st","reward_raw":"35,000 Coin","reward_type":["coin"],"reward_value_jpy":35000},
    {"rank":"1st","reward_raw":"THE GOLDEN CIRCLE TICKET","reward_type":["ticket"],"reward_value_jpy":null},
    {"rank":"2nd","reward_raw":"15,000 Coin","reward_type":["coin"],"reward_value_jpy":15000}
  ],
  "prizes_original":"1位: 35,000 Coin + THE GOLDEN CIRCLE TICKET / 2位: 15,000 Coin",
  "address":"東京都新宿区歌舞伎町1丁目25番3号 西武新宿駅前ビル（WAMALL）3階",
  "prefecture":"東京都",
  "city_ward":"新宿区",
  "tel":"03-6233-8879",
  "prizes_analyze": {
    "total_winners": 2,
    "total_value_jpy": 50000,
    "reward_categories": ["coin","ticket"],
    "rank_list": [
      {"rank":"1st","reward_summary":"35000円 + チケット1枚","reward_value_jpy":35000},
      {"rank":"2nd","reward_summary":"15000円","reward_value_jpy":15000}
    ]
  }
}
"""



# USER_PROMPT（每次调用只传入 Markdown 内容）
USER_PROMPT_TEMPLATE = """
以下の Markdown テキストからトーナメント情報を抽出分析し、SYSTEM_PROMPT に従って JSON 形式で出力してください。

Markdown 内容：
{markdown_content}

"""


def extract_json(markdown_text):
    prompt = USER_PROMPT_TEMPLATE.format(markdown_content=markdown_text)
    response = client.responses.parse(
        model="gpt-4o-mini",  # 或 gpt-4o-mini ,gpt-5-nano
        instructions=SYSTEM_PROMPT,
        input=prompt
    )
    return response.output_text



if __name__ == "__main__":
    # 遍历 Markdown 文件夹
    markdown_files = glob("backend/scripts/py-script/md_files/tourney/*.md")
    print('markdown_files: ' + str(len(markdown_files)))
    i = 0
    for md_file in markdown_files:
      if i > 3:
          break
      i += 1
      with open(md_file, 'r', encoding='utf-8') as f:
          md_text = f.read()

      json_output = extract_json(md_text)

      # 保存 JSON 结果
      out_path = md_file.replace("md_files", "json").replace(".md", ".json")
      os.makedirs(os.path.dirname(out_path), exist_ok=True)
      with open(out_path, 'w', encoding='utf-8') as f_out:
          f_out.write(json_output)

      print(f"✅ 处理完成：{md_file}")

