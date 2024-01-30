USE [Hotel]
GO

/****** Object:  UserDefinedFunction [dbo].[sf_ZiBuchungExist]    Script Date: 26.01.2023 13:52:30 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE OR ALTER   FUNCTION [dbo].[sf_ZiBuchungExist]
(
	-- Add the parameters for the function here
	@ZiBuchungsID int, --IN-Param
	@Datum    date     --IN-Param
)
RETURNS bit
AS
BEGIN
   DECLARE @CheckZiBuchungExist bit;
   

   SET @CheckZiBuchungExist =
(
	SELECT ZiBuchungsID
	FROM dbo.tb_ZimmerBuchung
	WHERE ZiBuchungsID = @ZiBuchungsID AND       --Buchungnummer exist und
		  (@Datum BETWEEN DatumVon AND DatumBis) --liegt im gültigen Zeitraum
)

IF  @CheckZiBuchungExist is NULL
	SET @CheckZiBuchungExist = 0
ELSE 
	SET @CheckZiBuchungExist = 1

RETURN @CheckZiBuchungExist;
END
GO


