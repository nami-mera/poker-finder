CREATE TABLE poker_shop (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自動増分ID',
    shop_name VARCHAR(100) NOT NULL COMMENT '店舗名',
    shop_id INT NOT NULL UNIQUE COMMENT '店舗固有ID（プラットフォームID）',
    shop_link VARCHAR(500) DEFAULT '' COMMENT '店舗リンク',
    address VARCHAR(200) DEFAULT '' COMMENT '店舗住所',
    map_link VARCHAR(500) DEFAULT '' COMMENT '地図リンク',
    phone VARCHAR(50) DEFAULT '' COMMENT '電話番号',
    homepage VARCHAR(200) DEFAULT '' COMMENT '公式ホームページURL',
    business_hours VARCHAR(200) DEFAULT '' COMMENT '営業時間',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時'
) COMMENT='ポーカーストア情報テーブル';

CREATE TABLE tournaments (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自動増分ID',
    event_id INT NOT NULL UNIQUE COMMENT 'トーナメント固有ID（プラットフォームID）',
    event_name VARCHAR(200) NOT NULL COMMENT 'トーナメント名',
    event_link VARCHAR(500) DEFAULT '' COMMENT 'トーナメント詳細リンク',
    status VARCHAR(50) NOT NULL DEFAULT 'upcoming' COMMENT 'ステータス（例: upcoming/ongoing/finished）',
    shop_id INT NOT NULL COMMENT '開催店舗ID',
    shop_name VARCHAR(100) DEFAULT '' COMMENT '開催店舗名（冗長/キャッシュ用）',
    official_page VARCHAR(200) DEFAULT '' COMMENT '公式ページリンク',
    start_time DATETIME NOT NULL COMMENT '開始日時',
    game_rule VARCHAR(200) DEFAULT '' COMMENT 'ゲームルール・ストラクチャ',
    entry_fee INT NOT NULL DEFAULT 0 COMMENT '参加費用（円）',
    re_entry VARCHAR(100) DEFAULT '' COMMENT 'リエントリー・ルール',
    prizes TEXT COMMENT '賞品情報の構造化データ（JSON）',
    prizes_original TEXT COMMENT '原文の賞品情報',
    address VARCHAR(200) DEFAULT '' COMMENT '開催場所住所',
    prefecture VARCHAR(200) DEFAULT '' COMMENT '都道府県（例: 東京都）',
    city_ward VARCHAR(200) DEFAULT '' COMMENT '市区町村（例: 新宿区）',
    tel VARCHAR(50) DEFAULT '' COMMENT '電話番号',
    total_winners INT NOT NULL DEFAULT 0 COMMENT '入賞人数',
    total_value_jpy INT NOT NULL DEFAULT 0 COMMENT '総賞金額（日本円換算）',
    reward_categories VARCHAR(200) DEFAULT '' COMMENT '賞品タイプ一覧（カンマ区切り）',
    rank_list TEXT COMMENT '各順位の賞品リスト（JSON形式）',
    reward_summary TEXT COMMENT '賞品に関する要約（合計・概要など）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    FOREIGN KEY (shop_id) REFERENCES poker_shop(shop_id) ON DELETE CASCADE
) COMMENT='ポーカートーナメント情報テーブル';

-- poker_shop テーブルの完全なINSERT文例
INSERT INTO poker_shop (
    shop_name,         -- 店舗名
    shop_id,           -- 店舗固有ID
    shop_link,         -- 店舗リンク
    address,           -- 店舗住所
    map_link,          -- 地図リンク
    phone,             -- 電話番号
    homepage,          -- 公式ホームページURL
    business_hours     -- 営業時間
    -- created_at,     -- 作成日時（自動生成）
    -- updated_at      -- 更新日時（自動生成）
) VALUES (
    'PokerStars Cafe',                           -- 店舗名
    1,                                           -- 店舗固有ID
    'https://pokerstarscafe.jp/',                -- 店舗リンク
    '東京都渋谷区宇田川町33-8 塚田ビルB1F',         -- 店舗住所
    'https://goo.gl/maps/1',                     -- 地図リンク
    '03-1234-5678',                              -- 電話番号
    'https://pokerstarscafe.jp/',                -- 公式ホームページURL
    '12:00-23:00'                                -- 営業時間
    -- created_atとupdated_atは省略（CURRENT_TIMESTAMP自動セット）
);

-- tournaments テーブルの完全なINSERT文例
INSERT INTO tournaments (
    event_id,            -- トーナメント固有ID
    event_name,          -- トーナメント名
    event_link,          -- トーナメント詳細リンク
    status,              -- ステータス（例: upcoming/ongoing/finished）
    shop_id,             -- 開催店舗ID
    shop_name,           -- 開催店舗名
    official_page,       -- 公式ページリンク
    start_time,          -- 開始日時
    game_rule,           -- ゲームルール
    entry_fee,           -- 参加費用（円）
    re_entry,            -- リエントリー・ルール
    prizes,              -- 賞品情報（JSONなど）
    prizes_original,     -- 原文の賞品情報
    address,             -- 開催場所住所
    prefecture,          -- 都道府県
    city_ward,           -- 市区町村
    tel,                 -- 電話番号
    total_winners,       -- 入賞人数
    total_value_jpy,     -- 総賞金額（日本円換算）
    reward_categories,   -- 賞品タイプ一覧
    rank_list,           -- 各順位の賞品リスト（JSON形式）
    reward_summary       -- 賞品まとめ
    -- created_at,       -- 作成日時（自動生成）
    -- updated_at        -- 更新日時（自動生成）
) VALUES (
    101,                                            -- トーナメント固有ID
    'Weekly No-Limit Hold\'em',                     -- トーナメント名
    'https://pokerstarscafe.jp/tournaments/101',    -- トーナメント詳細リンク
    'upcoming',                                     -- ステータス
    1,                                              -- 開催店舗ID
    'PokerStars Cafe',                              -- 開催店舗名
    'https://pokerstarscafe.jp/tournaments',        -- 公式ページリンク
    '2024-07-10 19:00:00',                          -- 開始日時
    'No-Limit Hold\'em',                            -- ゲームルール
    5000,                                           -- 参加費用（円）
    'Allowed once',                                 -- リエントリー・ルール
    '1st: 30000 JPY + Ticket\n2nd: 15000 JPY\n3rd: 10000 JPY + Ticket', -- 賞品情報
    '1st: 30000 JPY + Ticket\n2nd: 15000 JPY\n3rd: 10000 JPY + Ticket', -- 原文の賞品情報
    '東京都渋谷区宇田川町33-8 塚田ビルB1F',                             -- 開催場所住所
    '',                                             -- 都道府県（例: 東京都、現状空欄）
    '',                                             -- 市区町村（例: 新宿区、現状空欄）
    '03-1234-5678',                                 -- 電話番号
    3,                                              -- 入賞人数
    55000,                                          -- 総賞金額
    'Cash,Tickets',                                 -- 賞品タイプ一覧
    '[{"rank":"1st","reward_summary":"30000 JPY + Ticket","reward_value_jpy":30000},{"rank":"2nd","reward_summary":"15000 JPY","reward_value_jpy":15000},{"rank":"3rd","reward_summary":"10000 JPY + Ticket","reward_value_jpy":10000}]', -- 各順位賞品リスト
    ''                                              -- 賞品まとめ（現状空欄）
    -- created_atとupdated_atは省略（CURRENT_TIMESTAMP自動セット）
);