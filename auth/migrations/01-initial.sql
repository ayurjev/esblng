
CREATE DATABASE IF NOT EXISTS `auth`;
USE `auth`;

CREATE TABLE IF NOT EXISTS `credentials` (
    `Login` varchar(255) NOT NULL,
    `Password` varchar(32) NOT NULL,
    `Token` varchar(32) NOT NULL,
    `Created` datetime NOT NULL,
    PRIMARY KEY (`Login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
