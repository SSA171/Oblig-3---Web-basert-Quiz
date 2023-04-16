CREATE TABLE `User_answers` (
  `idUser_answers` INT NOT NULL AUTO_INCREMENT,
  `quest_id` INT NOT NULL,
  `idOpt` INT NOT NULL,
  `idUser` INT NOT NULL,
  `idResults` INT NOT NULL,
  PRIMARY KEY (`idUser_answers`),
  INDEX `quest_id_idx` (`quest_id` ASC) VISIBLE,
  INDEX `idOpt_idx` (`idOpt` ASC) VISIBLE,
  INDEX `idUser_idx` (`idUser` ASC) VISIBLE,
  INDEX `idResults_idx` (`idUser` ASC) VISIBLE,
  
  CONSTRAINT `questID`
    FOREIGN KEY (`quest_id`)
    REFERENCES `Questions` (`idQuest`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
	
  CONSTRAINT `optID`
    FOREIGN KEY (`idOpt`)
    REFERENCES `Options` (`idOpt`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    
	CONSTRAINT `userID`
    FOREIGN KEY (`idUser`)
    REFERENCES `Users` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    
	CONSTRAINT `resultsID`
    FOREIGN KEY (`idResults`)
    REFERENCES `Results` (`idResults`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)

ENGINE = InnoDB;

INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (1,1,1,1);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (2,5,1,1);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (3,9,1,1);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (4,13,1,1);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (5,19,1,1);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (6,24,1,1);

INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (1,1,1,2);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (2,5,1,2);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (3,10,1,2);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (4,14,1,2);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (5,20,1,2);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (6,23,1,2);

INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (1,1,1,3);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (2,5,1,3);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (3,10,1,3);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (4,15,1,3);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (5,20,1,3);
INSERT INTO `User_answers`(`quest_id`,`idOpt`,`idUser`,`idResults`) VALUES (6,23,1,3);



