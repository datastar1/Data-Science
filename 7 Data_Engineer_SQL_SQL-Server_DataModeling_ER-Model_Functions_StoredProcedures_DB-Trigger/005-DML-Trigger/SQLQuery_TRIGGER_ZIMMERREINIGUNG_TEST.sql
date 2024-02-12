USE [Hotel];
GO

INSERT INTO [dbo].[tb_ZimmerBuchung]
           ([ZimmerID], [DatumVon], [DatumBis])
     VALUES
           (2, '20-04-2023', '22-04-2023'); 
		   --Zimmer 2 , vom 20.04.2023 bis 22.04.2023

--SELECT *
--  FROM [FirmaUebung].[dbo].[View_Arbeitszeit]
--  WHERE Datum >= '01-01-2023'
--  ORDER BY Datum DESC, MaNN;

SELECT *
  FROM [dbo].[tb.Zimmerreinigung]
