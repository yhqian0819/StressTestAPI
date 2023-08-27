CREATE DATABASE IF NOT EXISTS stresstest;
USE stresstest;

CREATE TABLE `stresstest`.`pessoa` (
  `id` BINARY(16) NOT NULL,
  `apelido` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nome` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nascimento` DATE NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE (`apelido`),
  FULLTEXT INDEX (`apelido`, `nome`) WITH PARSER ngram
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `stresstest`.`pessoa_stacks` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pessoa_id` BINARY(16) NOT NULL,
  `stack` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  INDEX (`pessoa_id`),
  FULLTEXT INDEX (`stack`) WITH PARSER ngram,
  FOREIGN KEY (`pessoa_id`) REFERENCES `pessoa` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;