USE [Hotel]
GO

ALTER TABLE [dbo].[tb_ZimmerBuchung] DROP CONSTRAINT [CK_tb_DatumBis]
GO

ALTER TABLE [dbo].[tb_ZimmerBuchung]  WITH CHECK ADD  CONSTRAINT [CK_tb_DatumBis] CHECK  (([DatumBis]>=[DatumVon]))
GO

ALTER TABLE [dbo].[tb_ZimmerBuchung] CHECK CONSTRAINT [CK_tb_DatumBis]
GO


