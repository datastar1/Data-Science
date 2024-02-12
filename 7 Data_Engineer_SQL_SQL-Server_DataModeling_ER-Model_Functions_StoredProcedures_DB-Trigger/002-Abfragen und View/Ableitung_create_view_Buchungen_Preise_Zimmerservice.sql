------Einzelpreise Service
SELECT   dbo.tb_ZimmerBuchung.ZiBuchungsID, dbo.[tb.Zimmerservice].Datum, dbo.[tb.Zimmerservice].Preis, [dbo].[tb.Zimmerservice].ZiServiceID
		FROM     dbo.[tb.Zimmerservice] RIGHT OUTER JOIN dbo.tb_ZimmerBuchung
				 ON dbo.[tb.Zimmerservice].ZiBuchungsID = dbo.tb_ZimmerBuchung.ZiBuchungsID
		ORDER BY dbo.tb_ZimmerBuchung.ZiBuchungsID
-------Summe Service
SELECT   dbo.tb_ZimmerBuchung.ZiBuchungsID,  sum(dbo.[tb.Zimmerservice].Preis) AS GESAMT
		FROM     dbo.[tb.Zimmerservice] RIGHT OUTER JOIN dbo.tb_ZimmerBuchung
				 ON dbo.[tb.Zimmerservice].ZiBuchungsID = dbo.tb_ZimmerBuchung.ZiBuchungsID
		GROUP BY dbo.tb_ZimmerBuchung.ZiBuchungsID
-------ZimmerBuchungen
SELECT        dbo.tb_ZimmerBuchung.ZiBuchungsID, dbo.tb_ZimmerBuchung.DatumBis, dbo.tb_ZimmerBuchung.DatumVon,
						dbo.tb_ZiKategorie.Preis AS ZimmerPreis, dbo.tb_ZiKategorie.Typ, dbo.tb_Zimmer.Nummer,
						DATEDIFF( DAY , dbo.tb_ZimmerBuchung.DatumVon , dbo.tb_ZimmerBuchung.DatumBis) AS ANZAHL,
						(DATEDIFF( DAY , dbo.tb_ZimmerBuchung.DatumVon , dbo.tb_ZimmerBuchung.DatumBis) * dbo.tb_ZiKategorie.Preis) AS GESAMT
				
		FROM            dbo.tb_Zimmer INNER JOIN
								 dbo.tb_ZiKategorie ON dbo.tb_Zimmer.ZiKategorieID = dbo.tb_ZiKategorie.ZiKategorieID INNER JOIN
								 dbo.tb_ZimmerBuchung ON dbo.tb_Zimmer.ZimmerID = dbo.tb_ZimmerBuchung.ZimmerID



------------Gesamtpreis Service und Zimmer
SELECT C.ZiBuchungsID, sum(C.GESAMT) AS 'Alles zusammen'
FROM
(
SELECT A.ZiBuchungsID, A.GESAMT
FROM
		(SELECT   dbo.tb_ZimmerBuchung.ZiBuchungsID, 
		 
				 sum(dbo.[tb.Zimmerservice].Preis) AS GESAMT
		FROM     dbo.[tb.Zimmerservice] RIGHT OUTER JOIN dbo.tb_ZimmerBuchung
				 ON dbo.[tb.Zimmerservice].ZiBuchungsID = dbo.tb_ZimmerBuchung.ZiBuchungsID
		GROUP BY dbo.tb_ZimmerBuchung.ZiBuchungsID) AS A
UNION
SELECT B.ZiBuchungsID, B.GESAMT
FROM
		(SELECT        dbo.tb_ZimmerBuchung.ZiBuchungsID, 
						(DATEDIFF( DAY , dbo.tb_ZimmerBuchung.DatumVon , dbo.tb_ZimmerBuchung.DatumBis) * dbo.tb_ZiKategorie.Preis) AS GESAMT
				
		FROM            dbo.tb_Zimmer INNER JOIN
								 dbo.tb_ZiKategorie ON dbo.tb_Zimmer.ZiKategorieID = dbo.tb_ZiKategorie.ZiKategorieID INNER JOIN
								 dbo.tb_ZimmerBuchung ON dbo.tb_Zimmer.ZimmerID = dbo.tb_ZimmerBuchung.ZimmerID) AS B 
) AS C
GROUP BY C.ZiBuchungsID