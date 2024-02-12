USE [Hotel]
GO
/****** Object:  Table [dbo].[tb_TischBelegung]    Script Date: 25.01.2023 09:06:49 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tb_TischBelegung](
	[TischBelegungID] [int] IDENTITY(1,1) NOT NULL,
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
SET IDENTITY_INSERT [dbo].[tb_TischBelegung] ON 
GO
INSERT [dbo].[tb_TischBelegung] ([TischBelegungID], [TischID], [KundenID], [Datum], [ZahlPerson], [Kommentar]) VALUES (1, 1, 4, CAST(N'2023-01-25' AS Date), 1, N'am Fenster')
GO
INSERT [dbo].[tb_TischBelegung] ([TischBelegungID], [TischID], [KundenID], [Datum], [ZahlPerson], [Kommentar]) VALUES (2, 1, 4, CAST(N'2023-01-25' AS Date), 1, NULL)
GO
INSERT [dbo].[tb_TischBelegung] ([TischBelegungID], [TischID], [KundenID], [Datum], [ZahlPerson], [Kommentar]) VALUES (3, 8, 6, CAST(N'2023-01-26' AS Date), 1, NULL)
GO
INSERT [dbo].[tb_TischBelegung] ([TischBelegungID], [TischID], [KundenID], [Datum], [ZahlPerson], [Kommentar]) VALUES (4, 5, 6, CAST(N'2023-01-27' AS Date), 4, NULL)
GO
INSERT [dbo].[tb_TischBelegung] ([TischBelegungID], [TischID], [KundenID], [Datum], [ZahlPerson], [Kommentar]) VALUES (5, 2, 7, CAST(N'2023-02-23' AS Date), 4, NULL)
GO
INSERT [dbo].[tb_TischBelegung] ([TischBelegungID], [TischID], [KundenID], [Datum], [ZahlPerson], [Kommentar]) VALUES (6, 3, 7, CAST(N'2023-02-24' AS Date), 4, NULL)
GO
INSERT [dbo].[tb_TischBelegung] ([TischBelegungID], [TischID], [KundenID], [Datum], [ZahlPerson], [Kommentar]) VALUES (7, 1, 7, CAST(N'2023-02-25' AS Date), 4, NULL)
GO
SET IDENTITY_INSERT [dbo].[tb_TischBelegung] OFF
GO
ALTER TABLE [dbo].[tb_TischBelegung]  WITH CHECK ADD  CONSTRAINT [FK_tb_TischBelegung_tb_Kunden] FOREIGN KEY([KundenID])
REFERENCES [dbo].[tb_Kunden] ([KundenID])
GO
ALTER TABLE [dbo].[tb_TischBelegung] CHECK CONSTRAINT [FK_tb_TischBelegung_tb_Kunden]
GO
ALTER TABLE [dbo].[tb_TischBelegung]  WITH CHECK ADD  CONSTRAINT [FK_tb_TischBelegung_tb_Tisch] FOREIGN KEY([TischID])
REFERENCES [dbo].[tb_Tisch] ([TischID])
GO
ALTER TABLE [dbo].[tb_TischBelegung] CHECK CONSTRAINT [FK_tb_TischBelegung_tb_Tisch]
GO
ALTER TABLE [dbo].[tb_TischBelegung]  WITH CHECK ADD  CONSTRAINT [CK_tb_TischBelegung_Datum] CHECK  (([Datum]>=format(getdate(),'yyyyMMdd')))
GO
ALTER TABLE [dbo].[tb_TischBelegung] CHECK CONSTRAINT [CK_tb_TischBelegung_Datum]
GO
