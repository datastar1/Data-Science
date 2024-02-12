USE [Hotel]
GO

/****** Object:  View [dbo].[View_Buchung_Rechnungsbetrag]    Script Date: 26.01.2023 13:26:04 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[View_Buchung_Rechnungsbetrag]
AS
SELECT TOP (100) PERCENT dbo.tb_ZimmerBuchung.ZiBuchungsID, dbo.tb_ZimmerBuchung.ZimmerID, dbo.tb_ZiBuchungKunde.KundenID, dbo.tb_ZimmerBuchung.[Anzahl Tage], dbo.tb_ZiKategorie.Preis, 
                  dbo.tb_ZimmerBuchung.[Anzahl Tage] * dbo.tb_ZiKategorie.Preis AS Betrag
FROM     dbo.tb_ZimmerBuchung INNER JOIN
                  dbo.tb_ZiBuchungKunde ON dbo.tb_ZimmerBuchung.ZiBuchungsID = dbo.tb_ZiBuchungKunde.ZiBuchungsID INNER JOIN
                  dbo.tb_Zimmer ON dbo.tb_ZimmerBuchung.ZimmerID = dbo.tb_Zimmer.ZimmerID INNER JOIN
                  dbo.tb_ZiKategorie ON dbo.tb_Zimmer.ZiKategorieID = dbo.tb_ZiKategorie.ZiKategorieID
WHERE  (dbo.tb_ZiBuchungKunde.HauptkundeJaNein = 1)
ORDER BY dbo.tb_ZimmerBuchung.ZiBuchungsID
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[26] 4[21] 2[24] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "tb_ZiKategorie"
            Begin Extent = 
               Top = 7
               Left = 48
               Bottom = 296
               Right = 242
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "tb_Zimmer"
            Begin Extent = 
               Top = 38
               Left = 363
               Bottom = 179
               Right = 557
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "tb_ZimmerBuchung"
            Begin Extent = 
               Top = 19
               Left = 691
               Bottom = 287
               Right = 885
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "tb_ZiBuchungKunde"
            Begin Extent = 
               Top = 0
               Left = 1021
               Bottom = 254
               Right = 1243
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
      Begin ColumnWidths = 9
         Width = 284
         Width = 1200
         Width = 1200
         Width = 1200
         Width = 1200
         Width = 1200
         Width = 1200
         Width = 1200
         Width = 1200
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 12
         Column = 2640
         Alias = 900
         Table = 1176
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1356
         SortOrder = 1416
         GroupBy = 1350
         Filter = 1356
         Or = 1350
         Or = 1350
    ' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'View_Buchung_Rechnungsbetrag'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane2', @value=N'     Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'View_Buchung_Rechnungsbetrag'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=2 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'View_Buchung_Rechnungsbetrag'
GO


