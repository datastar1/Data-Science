/****** Skript für SelectTopNRows-Befehl aus SSMS ******/
SELECT TOP (1000) [TischBelegungID]
      ,[TischID]
      ,[KundenID]
      ,[Datum]
      ,[ZahlPerson]
      ,[Kommentar]
  FROM [Hotel].[dbo].[tb_TischBelegung]
  ORDER BY Datum;

--Der Zahl der Sitzplaetze ist 28

  SELECT [dbo].[sf_FreiSitzPlatz]('2023-01-28') -- alle frei

  SELECT [dbo].[sf_FreiSitzPlatz]('2023-01-26') -- ein Platz wird belegt

  SELECT [dbo].[sf_FreiSitzPlatz]('2023-01-25') -- zwei Plaetze werden belegt

  SELECT [dbo].[sf_FreiSitzPlatz]('2023-02-25') -- vier Plaetze werden belegt

