USE [Hotel]
GO

/****** Object:  StoredProcedure [dbo].[sp_Backup_Hotel_mit_Zeitstempel]    Script Date: 26.01.2023 09:47:37 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE OR ALTER   PROCEDURE [dbo].[sp_Backup_Hotel_mit_Zeitstempel]
	-- Add the parameters for the stored procedure here
	-- brauchen wir hier noch nicht
	
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	DECLARE @backupFile NVARCHAR(MAX); -- file name
    SET @backupFile = 'C:\SQL-Kurs\gruppenarbeit\backups\Hotel-'
    + [dbo].[sf_Zeitstempel]() 
    + '.bak'; 

    BACKUP DATABASE [Hotel] TO DISK = @backupFile;

	
   
END
GO


