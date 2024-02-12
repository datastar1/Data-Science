-- ================================================
-- Template generated from Template Explorer using:
-- Create Trigger (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- See additional Create Trigger templates for more
-- examples of different Trigger statements.
--
-- This block of comments will not be included in
-- the definition of the function.
-- ================================================
USE [Hotel];
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
CREATE OR ALTER TRIGGER tr_Zimmerreinigung_INSERT
   ON  [dbo].[tb_ZimmerBuchung]
   FOR INSERT

AS 
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	DECLARE @DatumID date;
	DECLARE @ZimmerID  smallint;
	DECLARE @ZiBUCHUNGSID int;
	DECLARE @PersonalID int;
	
	
	
	SELECT @DatumID = Datumbis FROM inserted
	SELECT @ZimmerID = ZimmerID FROM inserted
	SELECT @ZiBUCHUNGSID = ZiBuchungsID FROM inserted
	 
	BEGIN
	
		SET @PersonalID = 
		(
		[dbo].[sf_faule_Putzkraft]()
		);

    -- Insert statements for trigger here
		INSERT INTO [dbo].[tb.Zimmerreinigung]
	(
	ZiBuchungsID, ZimmerID , PersonalID,  Datum
	)
		VALUES (@ZiBUCHUNGSID, @ZimmerID, @PersonalID,  @DatumID);
		
	
	END
	

END
GO
