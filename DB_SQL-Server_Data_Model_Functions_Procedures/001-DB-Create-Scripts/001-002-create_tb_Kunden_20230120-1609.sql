USE [Hotel]
GO

ALTER TABLE [dbo].[tb_Kunden] DROP CONSTRAINT [CK_tb_Kreditkarte]
GO

/****** Object:  Table [dbo].[tb_Kunden]    Script Date: 20.01.2023 16:11:08 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[tb_Kunden]') AND type in (N'U'))
DROP TABLE [dbo].[tb_Kunden]
GO

/****** Object:  Table [dbo].[tb_Kunden]    Script Date: 20.01.2023 16:11:08 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tb_Kunden](
	[KundenID] [int] IDENTITY(1,1) NOT NULL,
	[KundenName] [nvarchar](20) NOT NULL,
	[KundenOrt] [nvarchar](20) NOT NULL,
	[Kreditkarte] [nvarchar](16) NULL,
 CONSTRAINT [PK_tb_Kunden] PRIMARY KEY CLUSTERED 
(
	[KundenID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[tb_Kunden]  WITH CHECK ADD  CONSTRAINT [CK_tb_Kreditkarte] CHECK  ((len([Kreditkarte])=(16)))
GO

ALTER TABLE [dbo].[tb_Kunden] CHECK CONSTRAINT [CK_tb_Kreditkarte]
GO


