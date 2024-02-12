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
-- Description:	die Prozedur soll Eingangsparameter pr�fen 
-- und Daten in Tabelle 'Projektzuordnung' hinzuf�gen
-- =============================================
CREATE OR ALTER   PROCEDURE [dbo].[sp_AnlageZimmerservice_ASC]
	--Inputparameter
	@ZiBuchungsID int, --f�r Pr�fung 
	@Datum date,     --auf g�ltige Buchung
	@Preis money,
	@PersonalID int,  --f�r Pr�fung, ob Kellner
	

					
	
	--Outputparameter
	@Erfolg bit OUTPUT, -- geklappt oder nicht
	@Feedback VARCHAR(MAX) OUTPUT -- Fehlermeldungen etc.
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	DECLARE @msg AS nvarchar(MAX);
	DECLARE @CheckZiBuchungExist AS bit;

		
	DECLARE @CheckServicepersonal AS bit;
	
	
	-------------------------------------------------------------------	
	BEGIN TRY 

		-- Pr�fung auf g�ltige Zimmerbuchung
		SET @CheckZiBuchungExist = [dbo].[sf_ZiBuchungExist](@ZiBuchungsID, @Datum); 
		IF @CheckZiBuchungExist = 0 -- Buchung gibt es gar nicht oder nicht f�r diesen Termin
		BEGIN
		    
			SET @msg = 'Zu dieser Buchung leider kein Zimmerservice m�glich.';
			THROW 55000, @msg, 1;
			-- https://docs.microsoft.com/de-de/sql/t-sql/language-elements/throw-transact-sql?view=sql-server-ver15
		END
		IF @CheckZiBuchungExist = 1 -- Buchung g�ltig, weiter gehts
		
		--Pr�fung richtiges Personal
		SET @CheckServicepersonal = 
		(
		SELECT        dbo.[tb.Personal].PersoanlID
		FROM            dbo.[tb.Personal] INNER JOIN
                         dbo.tb_Funktion ON dbo.[tb.Personal].FunktionID = dbo.tb_Funktion.FunktionID
		WHERE        (dbo.tb_Funktion.FunktionID = 2 AND PersoanlID = @PersonalID)
		)

		IF @CheckServicepersonal IS NULL
		BEGIN
			SET @msg = 'MA mit PerosnalID ' + str(@PersonalID) + ' ist nicht im Service.';
			THROW 55001, @msg, 1;
		END
		ELSE
		SET @CheckServicepersonal = 1
		
		--Alle Pr�fungen OK. Jetzt wird bef�llt.
		--Eintrag in [dbo].[tb_ZimmerBuchung]			
				
		INSERT INTO [dbo].[tb.Zimmerservice] 
			   ([ZiBuchungsID], [Datum], [Preis], [PersonalID])
		VALUES (@ZiBuchungsID, @Datum, @Preis, @PersonalID )	
		
	

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


