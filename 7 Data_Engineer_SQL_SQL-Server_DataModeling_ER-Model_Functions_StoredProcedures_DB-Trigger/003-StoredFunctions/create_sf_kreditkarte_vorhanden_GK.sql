USE [Hotel]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE OR ALTER FUNCTION sf_Kreditkarte_vorhanden
(
	-- Add the parameters for the function here
	@KundenID int
)
RETURNS bit
AS
BEGIN
   DECLARE @kreditkarte_vorhanden bit;
   DECLARE @kreditkarteNr nvarchar(16);

   SET @kreditkarteNr =
(
	SELECT Kreditkarte
	FROM dbo.tb_Kunden
	WHERE KundenID = @KundenID
)

if @kreditkarteNr is NULL
	SET @kreditkarte_vorhanden = 0
ELSE 
	SET @kreditkarte_vorhanden = 1

RETURN @kreditkarte_vorhanden;
END
GO

