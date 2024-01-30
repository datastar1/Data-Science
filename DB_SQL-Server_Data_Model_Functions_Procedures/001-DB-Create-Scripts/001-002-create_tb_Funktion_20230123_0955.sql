USE [Hotel]
GO

/****** Object:  Table [dbo].[tb_Funktion]    Script Date: 23.01.2023 09:49:45 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[tb_Funktion]') AND type in (N'U'))
DROP TABLE [dbo].[tb_Funktion]
GO

/****** Object:  Table [dbo].[tb_Funktion]    Script Date: 23.01.2023 09:49:45 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tb_Funktion](
	[FunktionID] [int] NOT NULL,
	[Funktionsbezeichnung] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_tb_Funktion] PRIMARY KEY CLUSTERED 
(
	[FunktionID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


