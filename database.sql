CREATE DATABASE binance_insider
USE binance_insider;

-- Path: database.sql


CREATE TABLE `traders` (
  `uid` varchar(255) NOT NULL,
  `name` text DEFAULT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `trades` 
ALTER TABLE `traders` ADD PRIMARY KEY(`uid`);