USE [Hotel]
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
CREATE FUNCTION tf_passende_Zimmer 
(	
	-- Add the parameters for the function here
	@Personenzahl int
)
RETURNS TABLE 
AS
RETURN 
(
	SELECT dbo.tb_Zimmer.ZimmerID, dbo.tb_Zimmer.Nummer, dbo.tb_ZiKategorie.ZiKategorieID, dbo.tb_ZiKategorie.Typ, dbo.tb_ZiKategorie.MaxBelegung
      FROM     dbo.tb_ZiKategorie INNER JOIN
               dbo.tb_Zimmer ON dbo.tb_ZiKategorie.ZiKategorieID = dbo.tb_Zimmer.ZiKategorieID
			   WHERE dbo.tb_ZiKategorie.MaxBelegung >= @Personenzahl
)
GO
