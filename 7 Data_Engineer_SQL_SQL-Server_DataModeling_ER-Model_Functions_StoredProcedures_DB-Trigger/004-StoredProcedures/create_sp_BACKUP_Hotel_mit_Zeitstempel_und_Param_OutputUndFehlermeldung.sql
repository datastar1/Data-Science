USE Hotel;
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
CREATE OR ALTER PROCEDURE [sp_Backup_Hotel_mit_Zeitstempel_und_Param_OutputUndFehlermeldung]
	@Pfad nvarchar(MAX),	-- Parameter 1,--@Pfad soll so aussehen: 'C:\SQL-Kurs\gruppenarbeit\backups\' 
	@Feedback nvarchar(MAX) OUTPUT -- Parameter 2
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	BEGIN TRY
	
		DECLARE @backupFile NVARCHAR(MAX); -- file name
		SET @backupFile = @Pfad + 
						  'Hotel-' + [dbo].[sf_Zeitstempel]() + '.bak';
   
		BACKUP DATABASE [Hotel] TO DISK = @backupFile;
		SET @Feedback = CHAR(10) + 'Alles OK!';
	END TRY
	BEGIN CATCH	
		-- Version 1
		--SET @Feedback = 'Fehler!';

		-- Version 2: @Feedback liefert Fehlermeldung-- ERROR_NUMBER()
		-- ERROR_MESSAGE()
		-- https://docs.microsoft.com/de-de/sql/t-sql/functions/error-number-transact-sql?view=sql-server-ver15
		--------------------------------
		-- Fehler- und Ereignisreferenz (Datenbank-Engine)
		-- https://docs.microsoft.com/de-de/sql/relational-databases/errors-events/errors-and-events-reference-database-engine?view=sql-server-ver15
		----------------------------------
		SET @Feedback = ERROR_MESSAGE() + CHAR(10)-- Zeilenumbruch
						+ 'Fehler Nr. ' + CONVERT(varchar, ERROR_NUMBER()) + CHAR(10)
						+ 'Prozedur: '  + ERROR_PROCEDURE() + CHAR(10)
						+ 'Zeile Nr.: ' + CONVERT(varchar,  ERROR_LINE());	

	END CATCH
	
END
GO
