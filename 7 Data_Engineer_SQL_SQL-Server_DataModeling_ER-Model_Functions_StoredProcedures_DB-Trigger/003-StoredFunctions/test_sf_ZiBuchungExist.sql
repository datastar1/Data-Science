    DECLARE @ZiBuchungsID int, --IN-Param
	        @Datum    date  ;   --IN-Param

SET @ZiBuchungsID = 4
	set         @Datum = '2023.01.24'


	SELECT [dbo].[sf_ZiBuchungExist](@ZiBuchungsID,@Datum) AS 'EXIST'
