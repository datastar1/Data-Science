USE [Hotel]
GO

/****** Object:  Table [dbo].[tb_ZiKategorie]    Script Date: 20.01.2023 14:53:25 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tb_ZiKategorie](
	[ZiKategorieID] [int] IDENTITY(1,1) NOT NULL,
	[Typ] [nchar](30) NOT NULL,
	[MaxBelegung] [smallint] NOT NULL,
	[Preis] [money] NOT NULL,
 CONSTRAINT [PK_tb_ZiKategorie] PRIMARY KEY CLUSTERED 
(
	[ZiKategorieID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


