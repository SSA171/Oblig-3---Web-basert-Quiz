CREATE TABLE `Questions` (
  `idQuest` INT NOT NULL AUTO_INCREMENT,
  `quiz_id` INT NOT NULL,
  `question_text` TEXT NOT NULL,
  PRIMARY KEY (`idQuest`, `quiz_id`),
  UNIQUE INDEX `id_UNIQUE` (`idQuest` ASC) VISIBLE,
  INDEX `quizID_idx` (`quiz_id` ASC) VISIBLE,
  CONSTRAINT `quizID`
    FOREIGN KEY (`quiz_id`)
    REFERENCES `Quiz` (`idQuiz`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

INSERT INTO `Questions` (`idQuest`, `quiz_id`, `question_text`) VALUES (DEFAULT, 1, 'Which country is the largest by land area?');
INSERT INTO `Questions` (`idQuest`, `quiz_id`, `question_text`) VALUES (DEFAULT, 1, 'Which country is the smallest by land area?');
INSERT INTO `Questions` (`idQuest`, `quiz_id`, `question_text`) VALUES (DEFAULT, 1, 'Which country is the most populous in the world?');
INSERT INTO `Questions` (`idQuest`, `quiz_id`, `question_text`) VALUES (DEFAULT, 1, 'Which country has the highest GDP per capita?');
INSERT INTO `Questions` (`idQuest`, `quiz_id`, `question_text`) VALUES (DEFAULT, 1, 'Which country has the longest coastline?');
INSERT INTO `Questions` (`idQuest`, `quiz_id`, `question_text`) VALUES (DEFAULT, 1, 'Which country has the largest number of UNESCO World Heritage sites?');