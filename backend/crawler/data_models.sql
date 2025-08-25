CREATE TABLE poker_shop (
    id INT PRIMARY KEY AUTO_INCREMENT,
    shop_name VARCHAR(100),
    shop_id INT,
    shop_link VARCHAR(500),
    address VARCHAR(200),
    map_link VARCHAR(500),
    phone VARCHAR(50),
    homepage VARCHAR(200),
    business_hours VARCHAR(200)
);

CREATE TABLE tournaments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT,
    event_name VARCHAR(200),
    event_link VARCHAR(500),
    status VARCHAR(50),
    shop_id INT,
    shop_name VARCHAR(100),
    official_page VARCHAR(200),
    start_time VARCHAR(100),
    game_rule VARCHAR(200),
    entry_fee INT,
    re_entry VARCHAR(100),
    prizes TEXT,
    prizes_original TEXT,
    address VARCHAR(200),
    tel VARCHAR(50),
    total_winners INT,
    total_value_jpy INT,
    reward_categories VARCHAR(200),
    rank_list TEXT
);

alter table tournaments add column shop_name VARCHAR(100);