IF DB_ID('SynonymsDB') IS NULL CREATE DATABASE SynonymsDB;
GO
USE SynonymsDB;
IF OBJECT_ID('dbo.synonyms') IS NULL
BEGIN
  CREATE TABLE dbo.synonyms (
    id INT IDENTITY(1,1) PRIMARY KEY,
    word NVARCHAR(100) NOT NULL,
    synonyms NVARCHAR(MAX) NOT NULL
  );
END
GO
TRUNCATE TABLE dbo.synonyms;
INSERT INTO dbo.synonyms(word, synonyms) VALUES
('happy', 'glad,joyful,cheerful'),
('small', N'["tiny","little","mini"]'),
('fast',  'quick,rapid,speedy');
GO
