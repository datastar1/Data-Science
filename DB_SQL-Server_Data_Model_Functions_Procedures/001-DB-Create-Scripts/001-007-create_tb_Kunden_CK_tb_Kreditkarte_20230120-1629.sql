USE [Hotel]
GO

ALTER TABLE [dbo].[tb_Kunden] DROP CONSTRAINT [CK_tb_Kreditkarte]
GO

ALTER TABLE [dbo].[tb_Kunden]  WITH CHECK ADD  CONSTRAINT [CK_tb_Kreditkarte] CHECK  ((len([Kreditkarte])=(16)))
GO

ALTER TABLE [dbo].[tb_Kunden] CHECK CONSTRAINT [CK_tb_Kreditkarte]
GO


