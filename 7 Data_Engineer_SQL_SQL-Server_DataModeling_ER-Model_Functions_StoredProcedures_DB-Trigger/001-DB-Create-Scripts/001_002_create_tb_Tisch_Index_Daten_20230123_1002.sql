USE [Hotel]
GO
/****** Object:  Table [dbo].[tb_Tisch]    Script Date: 23.01.2023 09:37:56 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tb_Tisch](
	[TischID] [int] IDENTITY(1,1) NOT NULL,
	[TischNummer] [nchar](5) NOT NULL,
	[SitzPlatz] [tinyint] NOT NULL,
	[Kommentar] [ntext] NULL,
 CONSTRAINT [PK_tb_Tisch] PRIMARY KEY CLUSTERED 
(
	[TischID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[tb_Tisch] ON 
GO
INSERT [dbo].[tb_Tisch] ([TischID], [TischNummer], [SitzPlatz], [Kommentar]) VALUES (1, N'1    ', 2, N'am Fenster')
GO
INSERT [dbo].[tb_Tisch] ([TischID], [TischNummer], [SitzPlatz], [Kommentar]) VALUES (2, N'2    ', 2, N'am Fenster')
GO
INSERT [dbo].[tb_Tisch] ([TischID], [TischNummer], [SitzPlatz], [Kommentar]) VALUES (3, N'3    ', 2, NULL)
GO
INSERT [dbo].[tb_Tisch] ([TischID], [TischNummer], [SitzPlatz], [Kommentar]) VALUES (4, N'4    ', 2, NULL)
GO
INSERT [dbo].[tb_Tisch] ([TischID], [TischNummer], [SitzPlatz], [Kommentar]) VALUES (5, N'5    ', 4, N'am Fenster')
GO
INSERT [dbo].[tb_Tisch] ([TischID], [TischNummer], [SitzPlatz], [Kommentar]) VALUES (6, N'6    ', 4, NULL)
GO
INSERT [dbo].[tb_Tisch] ([TischID], [TischNummer], [SitzPlatz], [Kommentar]) VALUES (7, N'7    ', 6, NULL)
GO
INSERT [dbo].[tb_Tisch] ([TischID], [TischNummer], [SitzPlatz], [Kommentar]) VALUES (8, N'8    ', 6, NULL)
GO
SET IDENTITY_INSERT [dbo].[tb_Tisch] OFF
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_tb_TischNummer]    Script Date: 23.01.2023 09:37:56 ******/
CREATE UNIQUE NONCLUSTERED INDEX [IX_tb_TischNummer] ON [dbo].[tb_Tisch]
(
	[TischNummer] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
