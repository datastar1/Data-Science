USE [Hotel]
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde] DROP CONSTRAINT [FK_tb_ZiBuchungKunde_tb_ZimmerBuchung]
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde] DROP CONSTRAINT [FK_tb_ZiBuchungKunde_tb_Kunden]
GO

/****** Object:  Table [dbo].[tb_ZiBuchungKunde]    Script Date: 20.01.2023 16:11:55 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[tb_ZiBuchungKunde]') AND type in (N'U'))
DROP TABLE [dbo].[tb_ZiBuchungKunde]
GO

/****** Object:  Table [dbo].[tb_ZiBuchungKunde]    Script Date: 20.01.2023 16:11:55 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tb_ZiBuchungKunde](
	[ZiBuchungKuID] [int] IDENTITY(1,1) NOT NULL,
	[KundenID] [int] NOT NULL,
	[ZiBuchungsID] [int] NOT NULL,
	[Hauptkunde] [bit] NOT NULL,
 CONSTRAINT [PK_tb_ZiBuchungKunde] PRIMARY KEY CLUSTERED 
(
	[ZiBuchungKuID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde]  WITH CHECK ADD  CONSTRAINT [FK_tb_ZiBuchungKunde_tb_Kunden] FOREIGN KEY([KundenID])
REFERENCES [dbo].[tb_Kunden] ([KundenID])
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde] CHECK CONSTRAINT [FK_tb_ZiBuchungKunde_tb_Kunden]
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde]  WITH CHECK ADD  CONSTRAINT [FK_tb_ZiBuchungKunde_tb_ZimmerBuchung] FOREIGN KEY([ZiBuchungsID])
REFERENCES [dbo].[tb_ZimmerBuchung] ([ZiBuchungsID])
GO

ALTER TABLE [dbo].[tb_ZiBuchungKunde] CHECK CONSTRAINT [FK_tb_ZiBuchungKunde_tb_ZimmerBuchung]
GO


