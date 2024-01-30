USE Hotel;
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
CREATE OR ALTER FUNCTION sf_FreieTischPlaetze 
(
	@Datum date
)
RETURNS smallint
AS
BEGIN
	-- Declare the return variable here
	DECLARE @AnzTischPlaetze smallint,
			@AnzReservTischPlaetze smallint,
			@AnzFreieTischPlaetze smallint; 

	SET @AnzTischPlaetze = 
	(
		SELECT SUM([SitzPlatz])
	    FROM [Hotel].[dbo].[tb_Tisch]
	);

	SET @AnzReservTischPlaetze =
	(
		SELECT SUM(ZahlPerson)
		FROM dbo.tb_TischBelegung
		WHERE Datum = @Datum
		GROUP BY Datum
	);

	IF @AnzReservTischPlaetze IS NULL
		SET @AnzReservTischPlaetze = 0;

	SET @AnzFreieTischPlaetze = @AnzTischPlaetze - @AnzReservTischPlaetze;

	-- Return the result of the function
	RETURN @AnzFreieTischPlaetze;

END
GO

