use [Hotel]
GO
GRANT SELECT ON [dbo].[tb.Personal] TO [HotelUser_R_O]
GO
use [Hotel]
GO
GRANT SELECT ON [dbo].[View_Kunden_Nummer_GetDate] TO [HotelUser_R_O]
GO
use [Hotel]
GO
GRANT SELECT ON [dbo].[tb.Zimmerreinigung] TO [HotelUser_R_O]
GO
use [Hotel]
GO
GRANT EXECUTE ON [dbo].[sp_AnlageBuchung] TO [HotelUser_R_O]
GO
use [Hotel]
GO
GRANT EXECUTE ON [dbo].[sp_Backup_Hotel_mit_Zeitstempel_und_Param_OutputUndFehlermeldung] TO [HotelUser_R_O]
GO
