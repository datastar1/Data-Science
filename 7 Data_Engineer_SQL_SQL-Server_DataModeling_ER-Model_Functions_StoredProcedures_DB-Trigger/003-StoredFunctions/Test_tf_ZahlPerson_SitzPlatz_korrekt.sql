USE Hotel
GO

SELECT *
FROM [dbo].[tf_ZahlPerson_SitzPlatz_korrekt](5)-- F�r 5 Person gibt es zwei Tische;

SELECT *
FROM [dbo].[tf_ZahlPerson_SitzPlatz_korrekt](1)-- F�r 1 Person gibt es acht Tische;

SELECT *
FROM [dbo].[tf_ZahlPerson_SitzPlatz_korrekt](9)-- F�r 9 Person gibt kein;

