CREATE DATABASE IF NOT EXISTS `abw`;
use `abw`;

CREATE TABLE IF NOT EXISTS `tree` (
	`tree_id` VARCHAR(255) NOT NULL,
	`location` POINT NULL,
	`species` VARCHAR(255) NOT NULL,
	`owner` VARCHAR(255) NOT NULL,
	`plant_date` DATE NOT NULL,
	`visits` INT UNSIGNED NOT NULL,
	PRIMARY KEY (`tree_id`)
);

CREATE TABLE IF NOT EXISTS `images` (
	`url` VARCHAR(255) NOT NULL PRIMARY KEY
	-- easily extensible if we want to store more information about the image...
);

CREATE TABLE IF NOT EXISTS `tree_images` (
	`url` VARCHAR(255) NOT NULL,
	`tree_id` VARCHAR(255) NOT NULL, -- tree id
	PRIMARY KEY (`url`, `tree_id`)
);
