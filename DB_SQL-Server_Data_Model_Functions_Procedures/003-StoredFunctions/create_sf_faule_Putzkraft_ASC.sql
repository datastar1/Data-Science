USE [Hotel]
GO

/****** Object:  UserDefinedFunction [dbo].[sf_faule_Putzkraft]    Script Date: 26.01.2023 10:37:06 ******/
--liefert die PersonalID der Person mit Funktion Housekeeping, die bisher am wenigsten Zimmer gereinigt hat
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


-- =============================================
-- Author:		ASC>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE OR ALTER   FUNCTION [dbo].[sf_faule_Putzkraft] 
(
--keine Inputparameter	
)
RETURNS int
AS
BEGIN
	DECLARE @Ergebnis int;

	-- TODO ----------
	SET @Ergebnis = 
	(
	SELECT TOP 1 A.PersoanlID FROM --2. SELECT Anfang
	(SELECT        dbo.[tb.Personal].PersoanlID, COUNT(dbo.[tb.Zimmerreinigung].ZiReiniID) AS PUETZE                               --erster SELECT Anfang
	FROM            dbo.[tb.Personal] LEFT JOIN
                         dbo.[tb.Zimmerreinigung] ON dbo.[tb.Personal].PersoanlID = dbo.[tb.Zimmerreinigung].PersonalID INNER JOIN
                         dbo.tb_Funktion ON dbo.[tb.Personal].FunktionID = dbo.tb_Funktion.FunktionID

	WHERE dbo.tb_Funktion.FunktionID = 1
	GROUP BY dbo.[tb.Personal].PersoanlID) AS A	--Zw.Speicher für 1. SELECT																					--erster SELECT Ende
	ORDER BY A.PUETZE ASC          --2. SELECT Ende
	);
	-- Return the result of the function
	RETURN @Ergebnis;
END
GO


