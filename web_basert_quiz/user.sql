--
-- Tabellstruktur for tabell `user`
--
CREATE TABLE `user` (
  `user` varchar(32) COLLATE utf8_unicode_ci NOT NULL UNIQUE,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL DEFAULT '''''''                                ''''''',
  `role` varchar(16) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'user',
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- -----------------------------------------------------
-- Data for table `mydb`.`user`
-- -----------------------------------------------------

INSERT INTO `user` (`username`, `password`, `role`) VALUES ('adminr', '123', 'administrator');
INSERT INTO `user` (`username`, `password`, `role`) VALUES ('user', '321', 'user');
INSERT INTO `user` (`username`, `password`, `role`) VALUES ('cat123', 'test123', 'user');
INSERT INTO `user` (`username`, `password`, `role`) VALUES ('hello', 'test321', 'administrator');

