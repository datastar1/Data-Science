USE [Hotel]
GO

/****** Object:  UserDefinedFunction [dbo].[sf_ZimmerFrei]    Script Date: 26.01.2023 22:57:49 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


-- =============================================
-- Author:		ASC
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE OR ALTER   FUNCTION [dbo].[sf_ZimmerFrei] 
(
	@ZimmerIDneu int, @DatumVonneu date, @DatumBisneu date  --für Test ausgeklammert
)
RETURNS bit
AS
BEGIN --Funktion

--SELECT   *      
--FROM            dbo.tb_Kunden INNER JOIN
--                         dbo.tb_ZiBuchungKunde ON dbo.tb_Kunden.KundenID = dbo.tb_ZiBuchungKunde.KundenID INNER JOIN
--                         dbo.tb_ZimmerBuchung ON dbo.tb_ZiBuchungKunde.ZiBuchungsID = dbo.tb_ZimmerBuchung.ZiBuchungsID INNER JOIN
--                         dbo.tb_Zimmer ON dbo.tb_ZimmerBuchung.ZimmerID = dbo.tb_Zimmer.ZimmerID;

--SELECT   tb_ZimmerBuchung.ZimmerID, DatumVon, DatumBis      
--FROM            dbo.tb_Kunden INNER JOIN
--                         dbo.tb_ZiBuchungKunde ON dbo.tb_Kunden.KundenID = dbo.tb_ZiBuchungKunde.KundenID INNER JOIN
--                         dbo.tb_ZimmerBuchung ON dbo.tb_ZiBuchungKunde.ZiBuchungsID = dbo.tb_ZimmerBuchung.ZiBuchungsID INNER JOIN
--                         dbo.tb_Zimmer ON dbo.tb_ZimmerBuchung.ZimmerID = dbo.tb_Zimmer.ZimmerID

	--DECLARE @ZimmerIDneu int, @DatumVonneu date, @DatumBisneu date --für Test
	--SET @ZimmerIDneu = 1 SET @DatumVonneu = '21.01.2023' SET @DatumBisneu = '26.01.2023' --für Test
	DECLARE @ZimmerID int, @DatumVon date, @DatumBis date,  @Ergebnis bit;

	DECLARE Cursor_Belegungen CURSOR FOR
		SELECT  tb_ZimmerBuchung.ZimmerID, DatumVon, DatumBis      
		FROM    dbo.tb_ZiBuchungKunde INNER JOIN
                    dbo.tb_ZimmerBuchung ON dbo.tb_ZiBuchungKunde.ZiBuchungsID = dbo.tb_ZimmerBuchung.ZiBuchungsID INNER JOIN
                    dbo.tb_Zimmer ON dbo.tb_ZimmerBuchung.ZimmerID = dbo.tb_Zimmer.ZimmerID
		
		WHERE DatumBis >= @DatumVonneu
		ORDER BY DatumVon;

    SET @Ergebnis = 1  --erstmal ist das Zimmer frei

	OPEN Cursor_Belegungen; -- so was wie SET @Variable = Wert
	
	FETCH NEXT FROM Cursor_Belegungen INTO @ZimmerID, @DatumVon, @DatumBis; -- go to record 1
	WHILE @@FETCH_STATUS = 0  
	-- Die FETCH-Anweisung war erfolgreich...
		--  @@FETCH_STATUS --------------------
		-- https://docs.microsoft.com/de-de/sql/t-sql/functions/fetch-status-transact-sql?view=sql-server-ver15
		--	 0	Die FETCH-Anweisung war erfolgreich.
		--  -1	Die FETCH-Anweisung ist fehlgeschlagen, oder die Zeile war außerhalb des Resultsets.
		--  -2	Die abgerufene Zeile fehlt.
		--  -9	Der Cursor führt keinen Abrufvorgang aus.
	BEGIN	--Cursor
				
		IF
		(
		(@ZimmerIDneu = @ZimmerID) AND ((@Datumvonneu <= @DatumVon) AND (@DatumBisneu >  @DatumVon)) OR
		(@ZimmerIDneu = @ZimmerID) AND ((@Datumvonneu <  @DatumBis) AND (@DatumBisneu >  @DatumBis)) OR
		(@ZimmerIDneu = @ZimmerID) AND ((@Datumvonneu >= @DatumVon) AND (@DatumBisneu <= @DatumBis)) OR
		(@ZimmerIDneu = @ZimmerID) AND ((@Datumvonneu <= @DatumVon) AND (@DatumBisneu >  @DatumBis))
		) --END IF
		BEGIN
			SET @Ergebnis = 0  --für das Zimmer überschneiden sich die Termine
			--PRINT 'break'
			BREAK
		END
			FETCH NEXT FROM Cursor_Belegungen INTO @ZimmerID, @DatumVon, @DatumBis;   -- go to next record
	END -- Cursor

CLOSE Cursor_Belegungen;
DEALLOCATE Cursor_Belegungen; --Arbeitsspeicher freigeben

--PRINT @Ergebnis; --für Test
--	IF @Ergebnis = 0
--	PRINT 'Geht nicht!'
--	ELSE
--	PRINT 'Zimmer frei!'

RETURN @Ergebnis;
END --Funktion
GO


