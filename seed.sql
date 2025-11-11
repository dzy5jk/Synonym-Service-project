IF DB_ID('SynonymsDB') IS NULL
BEGIN
  CREATE DATABASE SynonymsDB;
END
GO
USE SynonymsDB;
IF OBJECT_ID('dbo.Synonyms','U') IS NULL
BEGIN
  CREATE TABLE dbo.Synonyms (
    WordId   INT IDENTITY(1,1) PRIMARY KEY,
    Word     NVARCHAR(128) NOT NULL,
    Synonyms NVARCHAR(MAX) NOT NULL  -- comma-separated list for simplicity
  );
END
GO
-- idempotent seed
MERGE dbo.Synonyms AS T
USING (VALUES
  (N'fast', N'quick,rapid,speedy'),
  (N'smart', N'intelligent,clever,bright'),
  (N'happy', N'glad,joyful,content')
) AS S(Word,Synonyms)
ON T.Word = S.Word
WHEN NOT MATCHED THEN INSERT(Word,Synonyms) VALUES(S.Word,S.Synonyms);
GO
