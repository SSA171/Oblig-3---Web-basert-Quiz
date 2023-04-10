CREATE TABLE `Options` (
  `idOpt` INT NOT NULL AUTO_INCREMENT,
  `quest_id` INT NOT NULL,
  `option_text` TEXT NOT NULL,
  `is_correct` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`idOpt`, `quest_id`),
  UNIQUE INDEX `idOpt_UNIQUE` (`idOpt` ASC) VISIBLE,
  INDEX `quesID_idx` (`quest_id` ASC) VISIBLE,
  CONSTRAINT `quesID`
    FOREIGN KEY (`quest_id`)
    REFERENCES `Questions` (`idQuest`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 1, 'Russia', 1);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 1, 'China', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 1, 'USA', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 1, 'Brazil', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 2, 'Vatican City', 1);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 2, 'Monaco', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 2, 'Nauru', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 2, 'San Marino', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 3, 'India', DEFAULT );
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 3, 'China', 1);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 3, 'USA', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 3, 'Indonesia', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 4, 'Switzerland', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 4, 'Norway', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 4, 'Qatar', 1);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 4, 'Luxembourg', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 5, 'Russia', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 5, 'Australia', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 5, 'Indonesia', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 5, 'Canada', 1);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 6, 'Mexico', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 6, 'Italy', DEFAULT);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 6, 'China', 1);
INSERT INTO `Options` (idOpt, quest_id, option_text, is_correct) VALUES (DEFAULT, 6, 'Spain', DEFAULT);