CREATE TABLE `Quiz` (
  `idQuiz` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idQuiz`),
  UNIQUE INDEX `idQuiz_UNIQUE` (`idQuiz` ASC) VISIBLE)
ENGINE = InnoDB;

INSERT INTO `Quiz` (`idQuiz`, `title`) VALUES (DEFAULT, 'Country Quiz');


