USE Hotel;

go

Declare @ZiBuchungsID int, @ZimmerID int, @zuzahlen money

set @ZimmerID = 2




SELECT  TOP 1 ZiBuchungsID, DatumBis --,
	--FIRST_VALUE(ZiBuchungsID) OVER (ORDER BY DatumBis DESC)
    FROM            dbo.tb_Rechnung RIGHT JOIN
                         dbo.tb_ZimmerBuchung ON dbo.tb_Rechnung.ZiBuchungID = dbo.tb_ZimmerBuchung.ZiBuchungsID
    WHERE        (ZimmerID = @ZimmerID) AND [RechnungID] IS NULL --AND (DatumBis <= @Datum)
    ORDER BY DatumBis DESC 
	
SELECT TOP 1  @ZiBuchungsID = ZiBuchungsID
    FROM            dbo.tb_Rechnung RIGHT JOIN
                         dbo.tb_ZimmerBuchung ON dbo.tb_Rechnung.ZiBuchungID = dbo.tb_ZimmerBuchung.ZiBuchungsID
    WHERE        (ZimmerID = @ZimmerID) AND [RechnungID] IS NULL--AND (DatumBis <= @Datum)
    ORDER BY DatumBis DESC

	print 'Buchungsnummer: '
	print @ZiBuchungsID

	SELECT [GESAMT] FROM [dbo].[View_Buchungen_Preise_Zimmerservice_komprimiert]
	WHERE @ZiBuchungsID = [ZiBuchungsID]

	SELECT @zuzahlen = [GESAMT] FROM [dbo].[View_Buchungen_Preise_Zimmerservice_komprimiert]
	WHERE @ZiBuchungsID = [ZiBuchungsID]

	PRINT @zuzahlen

	