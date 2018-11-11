
CREATE DATABASE IF NOT EXISTS `wallets`;
USE `wallets`;

CREATE TABLE IF NOT EXISTS `wallets` (
    `Login` varchar(255) NOT NULL,
    `BaseCurrency` tinyint(4) NOT NULL,
    `Balance` decimal(16,4) DEFAULT 0.0,
    PRIMARY KEY (`Login`, `BaseCurrency`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
