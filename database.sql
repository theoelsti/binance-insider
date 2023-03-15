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
    PRIMARY KEY (id),
    FOREIGN KEY (trader_uid) REFERENCES traders(uid)
);