USE [Hotel]
GO

/****** Object:  Table [dbo].[tb.Personal]    Script Date: 20.01.2023 13:57:11 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tb.Personal](
	[PersoanlID] [int] IDENTITY(1,1) NOT NULL,
	[PersonalName] [nvarchar](50) NOT NULL,
	[Funktion] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_Personal] PRIMARY KEY CLUSTERED 
(
	[PersoanlID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


