USE [Hotel]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	< ZahlPerson <= SitzPlatz >
-- =============================================
CREATE OR ALTER FUNCTION  [dbo].[tf_ZahlPerson_SitzPlatz_korrekt] 
(	
	@ZahlPerson tinyint
)
RETURNS TABLE 
AS
RETURN 
(
	SELECT [tb_Tisch].SitzPlatz 
	  ,tb_Tisch.TischID
	FROM [Hotel].[dbo].[tb_Tisch]
	WHERE @ZahlPerson  <= [tb_Tisch].SitzPlatz
)

GO


