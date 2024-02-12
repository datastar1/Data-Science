USE [HOTEL]
GO
--Übergabe der KundenID zu der geprüft werden soll ob eine Kreditkarte hinterlegt ist
select dbo.sf_Kreditkarte_vorhanden(2) AS Kreditkarte_vorhanden;