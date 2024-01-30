USE [Hotel]
GO

/****** Object:  Table [dbo].[tb_TischBelegung]    Script Date: 23.01.2023 08:54:55 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tb_TischBelegung](
	[TischBelegungID] [int] NOT NULL,
	[TischID] [int] NOT NULL,
	[KundenID] [int] NOT NULL,
	[Datum] [date] NOT NULL,
	[ZahlPerson] [tinyint] NOT NULL,
	[Kommentar] [ntext] NULL,
 CONSTRAINT [PK_tb_TischBelegung] PRIMARY KEY CLUSTERED 
(
	[TischBelegungID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


