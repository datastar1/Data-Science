USE Hotel
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
CREATE OR ALTER FUNCTION sf_FreiSitzPlatz
(
	@Datum date
)
RETURNS smallint
AS
BEGIN
	DECLARE @AnzSitzPlatz smallint;
	DECLARE @AnzPerson smallint;
	DECLARE @AnzFreiSitzPlatz smallint;

	SET @AnzSitzPlatz =
	(
	SELECT SUM([SitzPlatz])
	FROM [dbo].[tb_Tisch]
	);

	SET @AnzPerson =
	(
	SELECT SUM([ZahlPerson])
	FROM [dbo].[tb_TischBelegung]
	WHERE Datum = @Datum
	GROUP BY [Datum]
	);

	IF @AnzPerson IS NULL
	SET @AnzPerson = 0;

	SET @AnzFreiSitzPlatz = @AnzSitzPlatz - @AnzPerson;

	RETURN @AnzFreiSitzPlatz;

END
GO

