USE [Hotel]
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde] DROP CONSTRAINT [FK_tb_ZiBuchungKunde_tb_ZimmerBuchung]
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde]  WITH CHECK ADD  CONSTRAINT [FK_tb_ZiBuchungKunde_tb_ZimmerBuchung] FOREIGN KEY([ZiBuchungsID])
REFERENCES [dbo].[tb_ZimmerBuchung] ([ZiBuchungsID])
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde] CHECK CONSTRAINT [FK_tb_ZiBuchungKunde_tb_ZimmerBuchung]
GO


