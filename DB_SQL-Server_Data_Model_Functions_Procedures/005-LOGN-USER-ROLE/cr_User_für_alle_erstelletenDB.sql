USE [master]
GO
CREATE LOGIN [HotelUserFull] WITH PASSWORD=N'1234', DEFAULT_DATABASE=[Hotel], DEFAULT_LANGUAGE=[Deutsch], CHECK_EXPIRATION=OFF, CHECK_POLICY=OFF
GO
use [FirmaUebung];
GO
use [master];
GO
USE [FirmaUebung]
GO
CREATE USER [HotelUserFull] FOR LOGIN [HotelUserFull]
GO
use [Hotel];
GO
use [FirmaUebung];
GO
USE [Hotel]
GO
CREATE USER [HotelUserFull] FOR LOGIN [HotelUserFull]
GO
use [Mietwagen];
GO
use [Hotel];
GO
USE [Mietwagen]
GO
CREATE USER [HotelUserFull] FOR LOGIN [HotelUserFull]
GO
