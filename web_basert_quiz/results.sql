CREATE TABLE `Results` (
  `idResults` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `quiz_id` INT NOT NULL,
  `correct_answers` INT NOT NULL,
  `total_questions` INT NOT NULL,
  PRIMARY KEY (`idResults`),
  INDEX `userID_idx` (`user_id` ASC) VISIBLE,
  INDEX `quizID_idx` (`quiz_id` ASC) VISIBLE,
  
  CONSTRAINT `userID_result`
    FOREIGN KEY(`user_id`)
    REFERENCES `Users` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    
  CONSTRAINT `quizID_result`
    FOREIGN KEY(`quiz_id`)
    REFERENCES `Quiz` (`idQuiz`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)

ENGINE = InnoDB;

INSERT INTO `Results` (`user_id`, `quiz_id`, `correct_answers`, `total_questions`) VALUES (1, 1, 2, 6);
INSERT INTO `Results` (`user_id`, `quiz_id`, `correct_answers`, `total_questions`) VALUES (1, 1, 5, 6);
INSERT INTO `Results` (`user_id`, `quiz_id`, `correct_answers`, `total_questions`) VALUES (1, 1, 6, 6);