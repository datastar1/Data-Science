USE [Hotel]
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde] DROP CONSTRAINT [FK_tb_ZiBuchungKunde_tb_Kunden]
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde]  WITH CHECK ADD  CONSTRAINT [FK_tb_ZiBuchungKunde_tb_Kunden] FOREIGN KEY([KundenID])
REFERENCES [dbo].[tb_Kunden] ([KundenID])
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde] CHECK CONSTRAINT [FK_tb_ZiBuchungKunde_tb_Kunden]
GO


