USE [Hotel]
GO

/****** Object:  Table [dbo].[tb.Zimmerservice]    Script Date: 20.01.2023 15:38:58 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO
DROP TABLE [dbo].[tb.Zimmerservice]
CREATE TABLE [dbo].[tb.Zimmerservice](
	[ZiServiceID] [int] IDENTITY(1,1) NOT NULL,
	[ZiBuchungsnummer] [nchar](5) NOT NULL,
	[Preis] [money] NOT NULL,
	[PersonalID] [int] NOT NULL,
	[Datum] [date] NOT NULL,
 CONSTRAINT [PK_tb.Zimmerservice] PRIMARY KEY CLUSTERED 
(
	[ZiServiceID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


