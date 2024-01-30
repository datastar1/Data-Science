USE Hotel
GO
-- ================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		ASC
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE OR ALTER PROCEDURE [dbo].[sp_Rechnungserstellung_ASC]

	-- Add the parameters for the stored procedure here
	--IN-Param
	@ZimmerID int,
	

--Outputparameter
	@Erfolg bit OUTPUT,				-- geklappt oder nicht
	@Feedback VARCHAR(MAX) OUTPUT -- Fehlermeldungen etc.
AS
BEGIN--ganz
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	 -- Insert statements for procedure here
	SET NOCOUNT ON;
	DECLARE @msg AS nvarchar(MAX);
   
	--Buchung ident.
	DECLARE @Datum date, @ZiBuchungsID int, @zuzahlen money
BEGIN TRY 
    
	SET @Datum = GETDATE()
	


	SELECT TOP 1  @ZiBuchungsID = ZiBuchungsID 
    FROM            dbo.tb_Rechnung RIGHT JOIN
                         dbo.tb_ZimmerBuchung ON dbo.tb_Rechnung.ZiBuchungID = dbo.tb_ZimmerBuchung.ZiBuchungsID
    WHERE        (ZimmerID = @ZimmerID) AND [RechnungID] IS NULL--AND (DatumBis <= @Datum)
    ORDER BY DatumBis DESC

	PRINT 'Buchungsnummer:'
	PRINT @ZiBuchungsID;

	IF  @ZiBuchungsID IS NULL
		BEGIN
			SET @msg = 'Keine offene Rechnung.';
			THROW 55001, @msg, 1;
		END

	--Gesamtbetrag holen und Rechnung buchen
	SELECT @zuzahlen = [GESAMT] FROM [dbo].[View_Buchungen_Preise_Zimmerservice_komprimiert]
	WHERE @ZiBuchungsID = [ZiBuchungsID]

	PRINT 'Zu zahlen: '
	PRINT @zuzahlen

	INSERT INTO [dbo].[tb_Rechnung]
					([ZiBuchungID], [Datum], [Betrag])
			VALUES  (@ZiBuchungsID, @Datum, @zuzahlen)



		SET @Erfolg = 1;
		SET @Feedback = 'Rechnung gebucht';

END TRY
BEGIN CATCH
		SET @Erfolg = 0; -- nicht geklappt--
		-- 	@Feedback text OUTPUT --Fehlermeldungen etc.
		SET @Feedback = 
			ERROR_MESSAGE() + ' Fehler Nr. '+ CONVERT(varchar, ERROR_NUMBER())
							+ ' Prozedur: '  + ERROR_PROCEDURE()
							+ ' Zeile Nr.: ' + CONVERT(varchar,  ERROR_LINE());
	END CATCH;    

END --ganz
GO
