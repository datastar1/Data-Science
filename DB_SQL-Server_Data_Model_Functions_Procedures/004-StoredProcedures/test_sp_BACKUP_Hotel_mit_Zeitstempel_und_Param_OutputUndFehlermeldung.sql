USE Hotel;
GO

DECLARE @Rueckgabe nvarchar(MAX); -- ist notwendig

---- Pfad existiert
EXEC [dbo].[sp_Backup_Firma_mit_Zeitstempel_und_Param_OutputUndFehlermeldung] 
	'C:\SQL-Kurs\gruppenarbeit\backups\',
	@Rueckgabe OUTPUT;




PRINT @Rueckgabe;