USE [Hotel]
GO

ALTER TABLE [dbo].[tb_ZimmerBuchung] DROP CONSTRAINT [DF_tb_ZimmerBuchung_DatumVon]
GO

ALTER TABLE [dbo].[tb_ZimmerBuchung] ADD  CONSTRAINT [DF_tb_ZimmerBuchung_DatumVon]  DEFAULT (getdate()) FOR [DatumVon]
GO


