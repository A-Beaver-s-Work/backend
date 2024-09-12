CREATE DATABASE IF NOT EXISTS `abw`;
use `abw`;

CREATE TABLE IF NOT EXISTS `tree` (
	`TreeID` VARCHAR(255) NOT NULL,
	`Location` POINT NULL,
	`Breed` VARCHAR(255) NOT NULL,
	`Owner` VARCHAR(255) NOT NULL,
	`DatePlanted` DATE NOT NULL,
	`Visits` INT UNSIGNED NOT NULL,
	PRIMARY KEY (`TreeID`)
);

CREATE TABLE IF NOT EXISTS `images` (
	`Filename` VARCHAR(255) NOT NULL PRIMARY KEY
	-- easily extensible if we want to store more information about the image...
);

CREATE TABLE IF NOT EXISTS `tree_images` (
	`Filename` VARCHAR(255) NOT NULL,
	`TreeID` VARCHAR(255) NOT NULL, -- tree id
	PRIMARY KEY (`Filename`, `TreeID`)
);
