
from openai import OpenAI
import os
from glob import glob
import logging
import json

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# SYSTEM_PROMPT（行为规则 + 输出规范 + 示例）

SYSTEM_PROMPT = """
あなたは、日本国内のポーカートーナメント情報に精通した分析アシスタントです。以下にあるMarkdown形式のトーナメント情報から、次の項目を推測・抽出してください。
抽出してほしい項目（フィールド）：
  start_date：開始日（例："2025-08-16" の形式）
  start_time：開始時間（例："11:30"）
  late_time：レイトレジスト締切時間（例："14:00"）
  chip_count：開始スタック（整数で、単位なし）
  entry_fee：参加費（円・整数のみ）
  re_entry：リエントリー・リバイ等のルール（例："5000円 / マルチリエントリー" や "1000円 / リエントリーのみ"）
  prefecture：都道府県（例："東京都"。記載がない場合は "東京都" としてください）
  city_ward：市区町村（例："新宿区", "渋谷市" 等）
  reward_summary：賞品の概要。（例："1st: 30000コイン + JOPTチケット3枚, 2nd: 15000コイン + SPADIEチケット1枚, 3rd: 10000コイン"， "1st　18:00-のトナメ エントリー無料, 2nd　エントリー半額"）
  reward_categories：出現した賞品カテゴリ一覧（例：["コイン", "SPADIE", "戦国", "JOPT", "招待券", "割引券"]）

注意点：
  出力は JSON形式のみ。余計な解説やテキストは不要です。
  金額はすべて整数で、単位は除く（例：1000円 → 1000）。
  prefecture（都道府県） が明記されていない場合は "東京都" をデフォルトで使用してください。
  reward_summary は複数の入場人数条件がある場合、最も多い人数帯に対応した内容を選んでください。
  reward_categories は報酬内容をもとに、次のようなカテゴリ名を自動で判断してください：
  コイン（ポイント）
  チケット（例：JOPT, SPADIE, 戦国など）
  店舗系賞品（例：割引券、招待券、エントリー無料など）

出力例：
{
  "start_date": "2025-08-16",
  "start_time": "11:30",
  "late_time": "14:00",
  "chip_count": 20000,
  "entry_fee": 5000,
  "re_entry": "5000円 / マルチリエントリー",
  "prefecture": "東京都",
  "city_ward": "新宿区",
  "reward_summary": "1st: 30000コイン + JOPTチケット3枚, 2nd: 15000コイン + SPADIEチケット1枚, 3rd: 10000コイン",
  "reward_categories": ["コイン", "SPADIE", "JOPT"]
}
"""


# USER_PROMPT（每次调用只传入 Markdown 内容）
USER_PROMPT_TEMPLATE = """
以下の Markdown テキストからトーナメント情報を抽出分析し、SYSTEM_PROMPT に従って JSON 形式で出力してください。

Markdown 内容：
{markdown_content}

"""


def query_ai(markdown_text):
    prompt = USER_PROMPT_TEMPLATE.format(markdown_content=markdown_text)
    response = client.responses.parse(
        model="gpt-4.1-nano",  # 或 gpt-4o-mini , gpt-5-nano, gpt-4.1-nano
        instructions=SYSTEM_PROMPT,
        input=prompt
    )
    logging.info(f"AI Response: {response.error}")
    return json.loads(response.output_text)



if __name__ == "__main__":
    # 遍历 Markdown 文件夹
    markdown_files = glob("backend/crawler/data/tournament/json_test/*")
    print('files: ' + str(len(markdown_files)))
    i = 0
    for md_file in markdown_files:
      if i >= 3:
          break
      i += 1
      with open(md_file, 'r', encoding='utf-8') as f:
          text = f.read()

      data = json.loads(text)
      json_output = query_ai(data["md_data"])

      # 保存 JSON 结果
      out_path = md_file.replace(".json", ".ai.json")
      os.makedirs(os.path.dirname(out_path), exist_ok=True)
      with open(out_path, 'w', encoding='utf-8') as f_out:
          f_out.write(json_output)

      print(f"✅ 处理完成：{md_file}")

