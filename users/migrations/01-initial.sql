
CREATE DATABASE IF NOT EXISTS `users`;
USE `users`;

CREATE TABLE IF NOT EXISTS `users` (
    `Login` varchar(255) NOT NULL,
    `Name` varchar(255) NOT NULL,
    `CountryID` int(11) DEFAULT NULL,
    `CityID` int(11) DEFAULT NULL,
    PRIMARY KEY (`Login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
