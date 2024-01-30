USE [Hotel]
GO

/****** Object:  StoredProcedure [dbo].[sp_AnlageBuchung_ASC]    Script Date: 25.01.2023 16:18:47 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		ASC
-- Create date: <Create Date,,>
-- Description:	die Prozedur soll Eingangsparameter prüfen 
-- und Daten in Tabelle 'Projektzuordnung' hinzufügen
-- =============================================
CREATE OR ALTER   PROCEDURE [dbo].[sp_AnlageBuchung_ASC]
	--Inputparameter
	@ZimmerID int, --für Prüfung Anlage tb_ZiBuchung
	@DatumVon date,
	@DatumBis date,

					
	@KundenID1 int,--für ZiBuKunde
	@KundenID2 int,
	@KundenID3 int,
	@KundenID4 int,
	--Outputparameter
	@Erfolg bit OUTPUT, -- geklappt oder nicht
	@Feedback VARCHAR(MAX) OUTPUT -- Fehlermeldungen etc.
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	DECLARE @msg AS nvarchar(MAX);
	DECLARE @CheckZiFrei AS bit;

	DECLARE @Anzahl tinyint,
			@Maxbelegung smallint;
	DECLARE	@table_Kunden TABLE (iID tinyint,iZahl int, iKundenID int)
	
	DECLARE @CheckHauptkunde AS bit;
	
	INSERT INTO  @table_Kunden     --für Befüllung [dbo].[tb_ZiBuchungKunde]
		VALUES  (1, 1, @KundenID1),
				(2, 1, @KundenID2),
				(3, 1, @KundenID3),
				(4, 1, @KundenID4);
	-------------------------------------------------------------------	
	BEGIN TRY 

		-- Prüfung auf freies Zimmer
		SET @CheckZiFrei = [dbo].[sf_ZimmerFrei](@ZimmerID,	@DatumVon, @DatumBis); 
		IF @CheckZiFrei = 0 -- Kein Zimmer
		BEGIN
		    
			SET @msg = 'ZimmerID ' + str(@ZimmerID) + ' nicht frei in diesem Zeitraum.';
			THROW 55000, @msg, 1;
			-- https://docs.microsoft.com/de-de/sql/t-sql/language-elements/throw-transact-sql?view=sql-server-ver15
		END
		IF @CheckZiFrei = 1 -- Zimmer frei, weiter gehts
		
		--Prüfung Maxbelegung
		SET @Anzahl = 0;
		SELECT @Anzahl = SUM(iZahl) FROM @table_Kunden
		WHERE iKundenID IS NOT NULL;
		
		SELECT @Maxbelegung = dbo.tb_ZiKategorie.MaxBelegung
		FROM            dbo.tb_ZiKategorie INNER JOIN
                         dbo.tb_Zimmer ON dbo.tb_ZiKategorie.ZiKategorieID = dbo.tb_Zimmer.ZiKategorieID
		WHERE [ZimmerID]=@ZimmerID
		
		IF  @Anzahl > @Maxbelegung
		BEGIN
			SET @msg = 'ZimmerID ' + str(@ZimmerID) + ' ist zu klein';
			THROW 55001, @msg, 1;
		END
		
		-- Prüfung, ob 1. Kunde KK hat
		
		SET @CheckHauptkunde = [dbo].[sf_Kreditkarte_vorhanden](@KundenID1)
		IF @CheckHauptkunde = 0 -- Kunde hat keine KK
		BEGIN
			SET @msg = '1. Kunde ' + str(@KundenID1) + ' kann nicht Hauptkunde sein, bitte HK zuerst eingeben.';
			THROW 55002, @msg, 1;
		END
		IF @CheckHauptkunde = 1 -- wir haben einen Hauptkunden, weiter gehts



		--Alle Prüfungen OK. Jetzt wird befüllt.
		--Eintrag in [dbo].[tb_ZimmerBuchung]			
		DECLARE @ZiBuchungsID int --für Prüfung Anlage tb_ZiBuKunde
		
		INSERT INTO [dbo].[tb_ZimmerBuchung] 
			   ([ZimmerID], [DatumVon], [DatumBis])
		VALUES (@ZimmerID,	@DatumVon, @DatumBis)	
		
		--neue @ZiBuchungsID schnappen
		SELECT SCOPE_IDENTITY() AS 'neue Buchungsnummer';
		SET @ZiBuchungsID = SCOPE_IDENTITY();
	

		--Eintrag aller Kunden in [dbo].[tb_ZiBuchungKunde]
		DECLARE @While tinyint,
				@InsertKundenID int,
				@InsertHK bit

		SET @While = 0
		WHILE @While < 4
		BEGIN --while
			SET @While = @WHILE + 1
			SELECT @InsertKundenID = iKundenID 
			FROM @table_Kunden 
			WHERE @While = iID

			IF @InsertKundenID IS NULL CONTINUE     --keine KundenID bitte nächste Zeile der @table_Kunden versuchen

			IF @While = 1							--nur erster Kunde ist HK
			SET @InsertHK = 1
			ELSE SET @InsertHK = 0

			INSERT INTO [dbo].[tb_ZiBuchungKunde]
					([ZiBuchungsID], [KundenID], [HauptkundeJaNein])
			VALUES  (@ZiBuchungsID, @InsertKundenID, @InsertHK)

		END--while



		SET @Erfolg = 1;
		SET @Feedback = 'Alles OK!';
	
	END TRY 
	BEGIN CATCH
		SET @Erfolg = 0; -- nicht geklappt--
		-- 	@Feedback text OUTPUT --Fehlermeldungen etc.
		SET @Feedback = 
			ERROR_MESSAGE() + ' Fehler Nr. '+ CONVERT(varchar, ERROR_NUMBER())
							+ ' Prozedur: '  + ERROR_PROCEDURE()
							+ ' Zeile Nr.: ' + CONVERT(varchar,  ERROR_LINE());
	END CATCH;    
END
GO


