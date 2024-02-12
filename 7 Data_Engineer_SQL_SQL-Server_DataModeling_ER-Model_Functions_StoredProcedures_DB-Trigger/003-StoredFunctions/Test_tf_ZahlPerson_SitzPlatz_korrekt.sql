USE Hotel
GO

SELECT *
FROM [dbo].[tf_ZahlPerson_SitzPlatz_korrekt](5)-- Für 5 Person gibt es zwei Tische;

SELECT *
FROM [dbo].[tf_ZahlPerson_SitzPlatz_korrekt](1)-- Für 1 Person gibt es acht Tische;

SELECT *
FROM [dbo].[tf_ZahlPerson_SitzPlatz_korrekt](9)-- Für 9 Person gibt kein;

