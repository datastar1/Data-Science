USE [HOTEL]
GO
--�bergabe der KundenID zu der gepr�ft werden soll ob eine Kreditkarte hinterlegt ist
select dbo.sf_Kreditkarte_vorhanden(2) AS Kreditkarte_vorhanden;