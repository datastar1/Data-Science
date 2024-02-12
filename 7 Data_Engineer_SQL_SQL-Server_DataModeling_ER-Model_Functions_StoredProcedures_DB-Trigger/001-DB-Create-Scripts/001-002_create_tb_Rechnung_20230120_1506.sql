USE [Hotel]
GO

/****** Object:  Table [dbo].[tb_Rechnung]    Script Date: 20.01.2023 15:06:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tb_Rechnung](
	[RechnungID] [int] IDENTITY(1,1) NOT NULL,
	[ZiBuchungID] [int] NOT NULL,
	[Datum] [date] NOT NULL,
	[Betrag] [money] NOT NULL,
 CONSTRAINT [PK_tb_Rechnung] PRIMARY KEY CLUSTERED 
(
	[RechnungID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[tb_Rechnung]  WITH CHECK ADD  CONSTRAINT [FK_tb_Rechnung_tb_Rechnung] FOREIGN KEY([RechnungID])
REFERENCES [dbo].[tb_Rechnung] ([RechnungID])
GO

ALTER TABLE [dbo].[tb_Rechnung] CHECK CONSTRAINT [FK_tb_Rechnung_tb_Rechnung]
GO


