/****** Skript für SelectTopNRows-Befehl aus SSMS ******/
SELECT TOP (1000) [TischBelegungID]
      ,[TischID]
      ,[KundenID]
      ,[Datum]
      ,[ZahlPerson]
      ,[Kommentar]
  FROM [Hotel].[dbo].[tb_TischBelegung]
  ORDER BY Datum;

  SELECT [dbo].[sf_FreieTischPlaetze]('2023-01-28') -- alle frei