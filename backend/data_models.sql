-- Active: 1756479388750@@127.0.0.1@3306@test
CREATE TABLE tournaments (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自動増分ID',
    event_id INT NOT NULL UNIQUE COMMENT 'トーナメント固有ID（プラットフォームID）',
    event_name VARCHAR(200) NOT NULL COMMENT 'トーナメント名',
    event_link VARCHAR(500) DEFAULT '' COMMENT 'トーナメント詳細リンク',
    start_date DATETIME NOT NULL COMMENT '開始日',
    start_time VARCHAR(20) DEFAULT '' COMMENT '開始日時',
    late_time VARCHAR(20) DEFAULT '' '遅刻時間',
    entry_fee INT NOT NULL DEFAULT 0 COMMENT '参加費用（円）',
    prizes_original TEXT COMMENT '原文の賞品情報',
    reward_categories VARCHAR(200) DEFAULT '' COMMENT '賞品タイプ一覧（coin, ticket, その他）',
    reward_summary TEXT COMMENT '賞品に関する要約（合計・概要など）',

    shop_id INT NOT NULL COMMENT '開催店舗ID',
    shop_name VARCHAR(100) DEFAULT '' COMMENT '開催店舗名',
    shop_link VARCHAR(200) DEFAULT '' COMMENT '開催店舗リンク',
    official_page VARCHAR(200) DEFAULT '' COMMENT '公式ページリンク',
    prefecture VARCHAR(200) DEFAULT '' COMMENT '都道府県（例: 東京都）',
    city_ward VARCHAR(200) DEFAULT '' COMMENT '市区町村（例: 新宿区）',

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時'
) COMMENT='ポーカートーナメント情報テーブル';


-- tournaments テーブルの完全なINSERT文例
INSERT INTO tournaments (
    event_id,            -- トーナメント固有ID
    event_name,          -- トーナメント名
    event_link,          -- トーナメント詳細リンク
    start_time,          -- 開始日時
    late_time,           -- 遅刻時間
    entry_fee,           -- 参加費用（円）
    prizes_original,     -- 原文の賞品情報
    reward_categories,   -- 賞品タイプ一覧
    reward_summary,      -- 賞品まとめ
    shop_id,             -- 開催店舗ID
    shop_name,           -- 開催店舗名
    shop_link,           -- 開催店舗リンク
    official_page,       -- 公式ページリンク
    address,             -- 開催場所住所
    prefecture,          -- 都道府県
    city_ward            -- 市区町村
    -- created_at,       -- 作成日時（自動生成）
    -- updated_at        -- 更新日時（自動生成）
) VALUES (
    101,                                            -- トーナメント固有ID
    'Weekly No-Limit Hold\'em',                     -- トーナメント名
    'https://pokerstarscafe.jp/tournaments/101',    -- トーナメント詳細リンク
    '2024-07-10 19:00:00',                          -- 開始日時
    '2024-07-10 19:30:00',                          -- 遅刻時間（例）
    5000,                                           -- 参加費用（円）
    '1st: 30000 JPY + Ticket\n2nd: 15000 JPY\n3rd: 10000 JPY + Ticket', -- 原文の賞品情報
    'Cash,Tickets',                                 -- 賞品タイプ一覧
    '',                                             -- 賞品まとめ（例：空欄）
    1,                                              -- 開催店舗ID
    'PokerStars Cafe',                              -- 開催店舗名
    'https://pokerstarscafe.jp/venues/101',        -- 開催店舗リンク
    'https://pokerstarscafe.jp/tournaments',        -- 公式ページリンク
    '東京都渋谷区宇田川町33-8 塚田ビルB1F',         -- 開催場所住所
    '東京都',                                       -- 都道府県
    '渋谷区'                                        -- 市区町村
    -- created_atとupdated_atは省略（CURRENT_TIMESTAMP自動セット）
);