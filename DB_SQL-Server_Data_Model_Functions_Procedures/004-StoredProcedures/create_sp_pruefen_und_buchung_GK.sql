USE [HOTEL]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================

-- Max 4 Bett Zimmer --> max 4 KundenIDs
CREATE OR ALTER PROCEDURE dbo.sp_pruefungen_und_buchung
	@Kunde_1_ID int, -- Hauptkunde
	@Kunde_2_ID int,
	@Kunde_3_ID int,
	@Kunde_4_ID int,
	@ZimmerID int,
	@DatumVon date,
	@DatumBIS date,

	------------------------------------------------
	@Erfolg bit OUTPUT, -- geklappt oder nicht
	@Feedback VARCHAR(MAX) OUTPUT -- Fehlermeldungen etc.

AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
    DECLARE @msg AS nvarchar(MAX); -- Fehlermeldung
	DECLARE @CheckResult AS int;		 
	DECLARE @RowID int;

	BEGIN TRY

	-- Eingangsparameter prüfen
	-- ????
	  


	  
	  
	  -- Mindestens 1 Kunde
	  IF @Kunde_1_ID IS NOT NULL
	  BEGIN --Begin if

	      -- Verfügbarkeitsprüfung: Zimmer frei im Zeitraum
		  -- Skalarwertfunktion
		  SET @CheckResult = [dbo].[sf_ZimmerFrei](@ZimmerID,@DatumVon,@DatumBIS) 
		  IF @CheckResult = 0  -- @ZimmerID nicht frei, Fehler
			  THROW 50001, 'ZimmerID nicht frei, Fehler, bitte prüfen!',1; 
          
		  -- Prüfung ob Hauptkunde: Kreditkarte in Tabelle Kunden hinterlegt
		  -- CURSOR
	      SET @CheckResult = [dbo].[sf_Kreditkarte_vorhanden](@Kunde_1_ID)
		  IF @CheckResult = 0  -- @Kunde_1_ID hat keine Kreditkarte hinterlegt
			  THROW 50003, 'Kunde_1_ID hat keine Kreditkarte hinterlegt, bitte prüfen!',1; 
          
		  -- Zimmerbuchung durchführen: Einträge Tabelle tb_ZimmerBuchung  
		  INSERT INTO [dbo].[tb_ZimmerBuchung]
             ([ZimmerId], [DatumVon], [DatumBis])
		  VALUES (@ZimmerID,@DatumVon, @DatumBIS);	 
		  
		  -- neue ZiBuchungsID herausfinden für Insert in Tabelle tb_ZiBuchungKunde
  	 	  SELECT SCOPE_IDENTITY() AS 'NeueBuchungsID';
		  SET @RowID = SCOPE_IDENTITY();

		  -- Einträge in Tabelle tb_ZiBuchungKunde - Zuordnung der Kunden zur Buchung
		  INSERT INTO [dbo].[tb_ZiBuchungKunde]
		  	  ([ZiBuchungsID], [KundenID], [HauptkundeJaNein])
		  VALUES (@RowID,@Kunde_1_ID,1) 

		  -- Weitere Kunden hinzufügen (leider kein array und for Schleife möglich)
		  		  IF @Kunde_2_ID IS NOT NULL
	      BEGIN --Begin if
		    INSERT INTO [dbo].[tb_ZiBuchungKunde]
		  	   ([ZiBuchungsID], [KundenID], [HauptkundeJaNein])
		    VALUES (@RowID,@Kunde_2_ID,0) 
          END   --END if

		  IF @Kunde_3_ID IS NOT NULL
	      BEGIN --Begin if
		    INSERT INTO [dbo].[tb_ZiBuchungKunde]
		  	   ([ZiBuchungsID], [KundenID], [HauptkundeJaNein])
		    VALUES (@RowID,@Kunde_3_ID,0) 
          END   --END if

		  IF @Kunde_4_ID IS NOT NULL
	      BEGIN --Begin if
		    INSERT INTO [dbo].[tb_ZiBuchungKunde]
		  	   ([ZiBuchungsID], [KundenID], [HauptkundeJaNein])
		    VALUES (@RowID,@Kunde_4_ID,0) 
          END   --END if

		  ----------------------
		  SET @Erfolg = 1;
	      SET @Feedback = 'Alles OK!';	
	  END --End if
	END TRY
	BEGIN CATCH
	  SET @Erfolg = 0; -- nicht geklappt--
	   -- 	@Feedback text OUTPUT --Fehlermeldungen etc.
	  SET @Feedback = 
			  ERROR_MESSAGE() + ' Fehler Nr. '+ CONVERT(varchar, ERROR_NUMBER())
				 		  + ' Prozedur: '  + ERROR_PROCEDURE()
						  + ' Zeile Nr.: ' + CONVERT(varchar,  ERROR_LINE());
	END CATCH;    
-- END -- End if
END