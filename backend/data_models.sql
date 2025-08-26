CREATE TABLE poker_shop (
    id INT PRIMARY KEY AUTO_INCREMENT,
    shop_name VARCHAR(100) NOT NULL,
    shop_id INT NOT NULL UNIQUE,
    shop_link VARCHAR(500) DEFAULT '',
    address VARCHAR(200) DEFAULT '',
    map_link VARCHAR(500) DEFAULT '',
    phone VARCHAR(50) DEFAULT '',
    homepage VARCHAR(200) DEFAULT '',
    business_hours VARCHAR(200) DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE tournaments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL UNIQUE,
    event_name VARCHAR(200) NOT NULL,
    event_link VARCHAR(500) DEFAULT '',
    status VARCHAR(50) NOT NULL DEFAULT 'upcoming',
    shop_id INT NOT NULL,
    shop_name VARCHAR(100) DEFAULT '',
    official_page VARCHAR(200) DEFAULT '',
    start_time DATETIME NOT NULL,
    game_rule VARCHAR(200) DEFAULT '',
    entry_fee INT NOT NULL DEFAULT 0,
    re_entry VARCHAR(100) DEFAULT '',
    prizes TEXT NOT NULL,
    prizes_original TEXT DEFAULT '',
    address VARCHAR(200) DEFAULT '',
    tel VARCHAR(50) DEFAULT '',
    total_winners INT NOT NULL DEFAULT 0,
    total_value_jpy INT NOT NULL DEFAULT 0,
    reward_categories VARCHAR(200) DEFAULT '',
    rank_list TEXT DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES poker_shop(shop_id) ON DELETE CASCADE
);