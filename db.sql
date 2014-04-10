SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `db` ;
CREATE SCHEMA IF NOT EXISTS `db` DEFAULT CHARACTER SET utf8 ;
USE `db` ;

-- -----------------------------------------------------
-- Table `db`.`Users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`Users` ;

CREATE TABLE IF NOT EXISTS `db`.`Users` (
  `email` VARCHAR(45) NOT NULL,
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `about` VARCHAR(255) NULL DEFAULT NULL,
  `isAnonymous` TINYINT NOT NULL DEFAULT 0,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `username` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`email`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`Forums`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`Forums` ;

CREATE TABLE IF NOT EXISTS `db`.`Forums` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `short_name` VARCHAR(45) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `short_name_UNIQUE` (`short_name` ASC),
  PRIMARY KEY (`short_name`),
  INDEX `fk_Forums_Users1` (`user` ASC),
  CONSTRAINT `fk_Forums_Users1`
    FOREIGN KEY (`user`)
    REFERENCES `db`.`Users` (`email`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`Threads`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`Threads` ;

CREATE TABLE IF NOT EXISTS `db`.`Threads` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATETIME NOT NULL,
  `dislikes` INT NOT NULL DEFAULT 0,
  `isClosed` TINYINT NOT NULL DEFAULT 0,
  `isDeleted` TINYINT NOT NULL DEFAULT 0,
  `likes` INT NOT NULL DEFAULT 0,
  `message` VARCHAR(150) NOT NULL,
  `points` INT NOT NULL DEFAULT 0,
  `parentDeleted` TINYINT NOT NULL DEFAULT 0,
  `slug` VARCHAR(50) NOT NULL,
  `title` VARCHAR(100) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  `forum` VARCHAR(45) NOT NULL,
  `posts` BIGINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `slug_UNIQUE` (`slug` ASC),
  INDEX `fk_Threads_Users1` (`user` ASC),
  INDEX `fk_Threads_Forums1` (`forum` ASC),
  CONSTRAINT `fk_Threads_Users1`
    FOREIGN KEY (`user`)
    REFERENCES `db`.`Users` (`email`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Threads_Forums1`
    FOREIGN KEY (`forum`)
    REFERENCES `db`.`Forums` (`short_name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`Posts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`Posts` ;

CREATE TABLE IF NOT EXISTS `db`.`Posts` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `date` DATETIME NOT NULL,
  `dislikes` INT NOT NULL DEFAULT 0,
  `isApproved` TINYINT NOT NULL DEFAULT 0,
  `isDeleted` TINYINT NOT NULL DEFAULT 0,
  `isEdited` TINYINT NOT NULL DEFAULT 0,
  `isHighlighted` TINYINT NOT NULL DEFAULT 0,
  `isSpam` TINYINT NOT NULL DEFAULT 0,
  `likes` INT NOT NULL DEFAULT 0,
  `user` VARCHAR(45) NOT NULL,
  `message` VARCHAR(255) NOT NULL,
  `points` INT NOT NULL DEFAULT 0,
  `parentDeleted` TINYINT NOT NULL DEFAULT 0,
  `thread` INT NOT NULL,
  `forum` VARCHAR(45) NOT NULL,
  `parent` BIGINT NULL DEFAULT NULL,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  PRIMARY KEY (`id`),
  INDEX `fk_Posts_Threads1` (`thread` ASC),
  INDEX `fk_Posts_Users1` (`user` ASC),
  INDEX `fk_Posts_Posts1` (`parent` ASC),
  INDEX `fk_Posts_Forums1` (`forum` ASC),
  CONSTRAINT `fk_Posts_Threads1`
    FOREIGN KEY (`thread`)
    REFERENCES `db`.`Threads` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Posts_Users1`
    FOREIGN KEY (`user`)
    REFERENCES `db`.`Users` (`email`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Posts_Posts1`
    FOREIGN KEY (`parent`)
    REFERENCES `db`.`Posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Posts_Forums1`
    FOREIGN KEY (`forum`)
    REFERENCES `db`.`Forums` (`short_name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`Followers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`Followers` ;

CREATE TABLE IF NOT EXISTS `db`.`Followers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `follower` VARCHAR(45) NOT NULL,
  `followee` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_Folowers_Users1` (`follower` ASC),
  INDEX `fk_Folowers_Users2` (`followee` ASC),
  CONSTRAINT `fk_Folowers_Users1`
    FOREIGN KEY (`follower`)
    REFERENCES `db`.`Users` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Folowers_Users2`
    FOREIGN KEY (`followee`)
    REFERENCES `db`.`Users` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`Subscriptions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`Subscriptions` ;

CREATE TABLE IF NOT EXISTS `db`.`Subscriptions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `thread` INT NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Subscriptions_Threads1` (`thread` ASC),
  INDEX `fk_Subscriptions_Users1` (`user` ASC),
  CONSTRAINT `fk_Subscriptions_Threads1`
    FOREIGN KEY (`thread`)
    REFERENCES `db`.`Threads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Subscriptions_Users1`
    FOREIGN KEY (`user`)
    REFERENCES `db`.`Users` (`email`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
