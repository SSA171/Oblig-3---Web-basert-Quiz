
-- -----------------------------------------------------
-- Table `Users`
-- -----------------------------------------------------
CREATE TABLE `Users` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(128) NOT NULL,
  `typeofuser` ENUM('administrator', 'user') NOT NULL,
  PRIMARY KEY (`idUser`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`idUser` ASC) VISIBLE)
ENGINE = InnoDB;

INSERT INTO `Users` (`idUser`, `username`, `password`, `typeofuser`) VALUES (1, 'user','\'pbkdf2:sha256:260000$V2i99ckU$8b0601a75b4c4b2c2bae10ea9fd1e40756156dc50887a11251c8a7904de43027\'', 'user');
INSERT INTO `Users` (`idUser`, `username`, `password`, `typeofuser`) VALUES (2, 'admin','\'pbkdf2:sha256:260000$V2i99ckU$8b0601a75b4c4b2c2bae10ea9fd1e40756156dc50887a11251c8a7904de43027\'', 'administrator');
INSERT INTO `Users` (`idUser`, `username`, `password`, `typeofuser`) VALUES (3, 'yuri','\'pbkdf2:sha256:260000$V2i99ckU$8b0601a75b4c4b2c2bae10ea9fd1e40756156dc50887a11251c8a7904de43027\'', 'administrator');
