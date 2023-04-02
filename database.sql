CREATE DATABASE binance_insider;
USE binance_insider;

-- Path: database.sql


CREATE TABLE `traders` (
  `uid` varchar(255) NOT NULL,
  `name` text DEFAULT NULL
)

CREATE TABLE `trades`;
ALTER TABLE `traders` ADD PRIMARY KEY(`uid`);


CREATE TABLE trades (
    id VARCHAR(64) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    entry_price FLOAT NOT NULL,
    mark_price FLOAT NOT NULL,
    pnl FLOAT NOT NULL,
    roe FLOAT NOT NULL,
    amount INT NOT NULL,
    update_timestamp BIGINT NOT NULL,
    leverage INT NOT NULL,
    telegram_message_id BIGINT,
    type INT NOT NULL,
    trader_uid VARCHAR(255) NOT NULL,
    announced_roe FLOAT,
    drawdown FLOAT,
    PRIMARY KEY (id),
    FOREIGN KEY (trader_uid) REFERENCES traders(uid)
);

CREATE TABLE subscription_tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR(32) NOT NULL UNIQUE,
    subscription_type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    claimed BOOLEAN DEFAULT FALSE
);

CREATE TABLE daily_trades (
    trade_id VARCHAR(64) PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    opened BIGINT NOT NULL,
    closed BIGINT NOT NULL,
    message_id INT NOT NULL,
    profit FLOAT NOT NULL
);

CREATE TABLE daily_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    profit FLOAT NOT NULL,
    total_trades INT NOT NULL,
    winning_trades INT NOT NULL,
    losing_trades INT NOT NULL
);
