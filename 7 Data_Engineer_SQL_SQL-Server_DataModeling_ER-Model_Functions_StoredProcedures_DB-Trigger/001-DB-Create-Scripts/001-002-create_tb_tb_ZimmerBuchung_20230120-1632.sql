USE [Hotel]
GO

ALTER TABLE [dbo].[tb_ZimmerBuchung] DROP CONSTRAINT [CK_tb_DatumBis]
GO

ALTER TABLE [dbo].[tb_ZimmerBuchung] DROP CONSTRAINT [DF_tb_ZimmerBuchung_DatumVon]
GO

/****** Object:  Table [dbo].[tb_ZimmerBuchung]    Script Date: 20.01.2023 16:31:24 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[tb_ZimmerBuchung]') AND type in (N'U'))
DROP TABLE [dbo].[tb_ZimmerBuchung]
GO

/****** Object:  Table [dbo].[tb_ZimmerBuchung]    Script Date: 20.01.2023 16:31:24 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tb_ZimmerBuchung](
	[ZiBuchungsID] [int] IDENTITY(1,1) NOT NULL,
	[KundenID] [int] NOT NULL,
	[ZimmerID] [int] NOT NULL,
	[DatumVon] [date] NOT NULL,
	[DatumBis] [date] NOT NULL,
 CONSTRAINT [PK_tb_ZimmerBuchung] PRIMARY KEY CLUSTERED 
(
	[ZiBuchungsID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[tb_ZimmerBuchung] ADD  CONSTRAINT [DF_tb_ZimmerBuchung_DatumVon]  DEFAULT (getdate()) FOR [DatumVon]
GO

ALTER TABLE [dbo].[tb_ZimmerBuchung]  WITH CHECK ADD  CONSTRAINT [CK_tb_DatumBis] CHECK  (([DatumBis]>=[DatumVon]))
GO

ALTER TABLE [dbo].[tb_ZimmerBuchung] CHECK CONSTRAINT [CK_tb_DatumBis]
GO


