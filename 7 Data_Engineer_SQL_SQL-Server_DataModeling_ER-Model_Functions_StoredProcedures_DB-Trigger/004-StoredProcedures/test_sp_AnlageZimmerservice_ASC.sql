USE Hotel;
GO

DECLARE @ZiBuchungsID int,	--für Prüfung 
		@Datum date,		--auf gültige Buchung
		@Preis money,
		@PersonalID int		--für Prüfung, ob Kellner
DECLARE	@Erfolg bit;		-- geklappt oder nicht
DECLARE	@Feedback VARCHAR(MAX); -- Fehlermeldungen etc.




EXEC [dbo].[sp_AnlageZimmerservice_ASC]
			4,		--@ZiBuchungsID int, --für Prüfung 
	'2023-01-25',	--@Datum date,     --auf gültige Buchung
			20,	--@Preis money,  frei
			2,	    --@PersonalID int,   --Prüfung ob Kellner






@Erfolg OUTPUT,
	@Feedback OUTPUT;


SELECT @Erfolg AS 'Geklappt?', @Feedback AS 'Rückgabemeldung';