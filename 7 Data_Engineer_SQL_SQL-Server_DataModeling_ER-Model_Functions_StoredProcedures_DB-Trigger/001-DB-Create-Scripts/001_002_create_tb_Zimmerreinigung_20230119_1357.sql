USE [Hotel]
GO

/****** Object:  Table [dbo].[tb.Zimmerreinigung]    Script Date: 20.01.2023 14:06:57 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tb.Zimmerreinigung](
	[ZiReiniID] [int] IDENTITY(1,1) NOT NULL,
	[ZimmerID] [int] NOT NULL,
	[PersonalID] [int] NOT NULL,
	[Datum] [date] NOT NULL,
 CONSTRAINT [PK_tb.Zimmerreinigung] PRIMARY KEY CLUSTERED 
(
	[ZiReiniID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


