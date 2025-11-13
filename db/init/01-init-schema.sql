SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema movies
-- -----------------------------------------------------
USE `movies`;

-- -----------------------------------------------------
-- Table `movies`.`actor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies`.`actor` (
  `act_id` INT NOT NULL,
  `act_fname` CHAR(20) NULL,
  `act_lname` CHAR(20) NULL,
  `act_gender` CHAR(1) NULL,
  PRIMARY KEY (`act_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `movies`.`director`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies`.`director` (
  `dir_id` INT NOT NULL,
  `dir_fname` CHAR(20) NULL,
  `dir_lname` CHAR(20) NULL,
  PRIMARY KEY (`dir_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `movies`.`movie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies`.`movie` (
  `mov_id` INT NOT NULL AUTO_INCREMENT,
  `mov_title` CHAR(50) NULL,
  `mov_year` INT NULL,
  `mov_time` INT NULL,
  `mov_lang` CHAR(50) NULL,
  `mov_dt_rel` CHAR(50) NULL,
  `mov_rel_country` CHAR(5) NULL,
  PRIMARY KEY (`mov_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `movies`.`reviewer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies`.`reviewer` (
  `rev_id` INT NOT NULL AUTO_INCREMENT,
  `rev_name` CHAR(30) NULL,
  PRIMARY KEY (`rev_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `movies`.`genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies`.`genres` (
  `gen_id` INT NOT NULL AUTO_INCREMENT,
  `gen_title` CHAR(20) NULL,
  PRIMARY KEY (`gen_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `movies`.`movie_direction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies`.`movie_direction` (
  `dir_id` INT NOT NULL,
  `mov_id` INT NOT NULL,
  PRIMARY KEY (`dir_id`, `mov_id`),
  INDEX `fk_movie_direction_movie1_idx` (`mov_id` ASC),
  CONSTRAINT `fk_movie_direction_director`
    FOREIGN KEY (`dir_id`)
    REFERENCES `movies`.`director` (`dir_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movie_direction_movie1`
    FOREIGN KEY (`mov_id`)
    REFERENCES `movies`.`movie` (`mov_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `movies`.`movie_cast`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies`.`movie_cast` (
  `role` CHAR(30) NULL,
  `mov_id` INT NOT NULL,
  `act_id` INT NOT NULL,
  PRIMARY KEY (`mov_id`, `act_id`),
  INDEX `fk_movie_cast_actor1_idx` (`act_id` ASC),
  CONSTRAINT `fk_movie_cast_movie1`
    FOREIGN KEY (`mov_id`)
    REFERENCES `movies`.`movie` (`mov_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movie_cast_actor1`
    FOREIGN KEY (`act_id`)
    REFERENCES `movies`.`actor` (`act_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `movies`.`movie_genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies`.`movie_genres` (
  `mov_id` INT NOT NULL,
  `gen_id` INT NOT NULL,
  PRIMARY KEY (`mov_id`, `gen_id`),
  INDEX `fk_movie_genres_genres1_idx` (`gen_id` ASC),
  CONSTRAINT `fk_movie_genres_movie1`
    FOREIGN KEY (`mov_id`)
    REFERENCES `movies`.`movie` (`mov_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movie_genres_genres1`
    FOREIGN KEY (`gen_id`)
    REFERENCES `movies`.`genres` (`gen_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `movies`.`rating`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies`.`rating` (
  `rev_stars` INT NULL,
  `num_o_ratings` INT NULL,
  `mov_id` INT NOT NULL,
  `rev_id` INT NOT NULL,
  PRIMARY KEY (`mov_id`, `rev_id`),
  INDEX `fk_rating_reviewer1_idx` (`rev_id` ASC),
  CONSTRAINT `fk_rating_movie1`
    FOREIGN KEY (`mov_id`)
    REFERENCES `movies`.`movie` (`mov_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rating_reviewer1`
    FOREIGN KEY (`rev_id`)
    REFERENCES `movies`.`reviewer` (`rev_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
