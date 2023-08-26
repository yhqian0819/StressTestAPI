CREATE DATABASE IF NOT EXISTS stresstest;
USE stresstest;

CREATE TABLE `pessoa` (
  `id` BINARY(16) DEFAULT (UUID_TO_BIN(UUID())) NOT NULL,
  `apelido` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nome` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nascimento` DATE NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE (`apelido`),
  FULLTEXT INDEX (`apelido`, `nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `pessoa_stacks` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pessoa_id` BINARY(16) NOT NULL,
  `stack` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  INDEX (`pessoa_id`),
  FULLTEXT INDEX (`stack`),
  FOREIGN KEY (`pessoa_id`) REFERENCES `pessoa` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;