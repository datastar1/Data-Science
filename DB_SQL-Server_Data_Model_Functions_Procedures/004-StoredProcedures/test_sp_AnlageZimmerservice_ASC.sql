USE Hotel;
GO

DECLARE @ZiBuchungsID int,	--f�r Pr�fung 
		@Datum date,		--auf g�ltige Buchung
		@Preis money,
		@PersonalID int		--f�r Pr�fung, ob Kellner
DECLARE	@Erfolg bit;		-- geklappt oder nicht
DECLARE	@Feedback VARCHAR(MAX); -- Fehlermeldungen etc.




EXEC [dbo].[sp_AnlageZimmerservice_ASC]
			4,		--@ZiBuchungsID int, --f�r Pr�fung 
	'2023-01-25',	--@Datum date,     --auf g�ltige Buchung
			20,	--@Preis money,  frei
			2,	    --@PersonalID int,   --Pr�fung ob Kellner






@Erfolg OUTPUT,
	@Feedback OUTPUT;


SELECT @Erfolg AS 'Geklappt?', @Feedback AS 'R�ckgabemeldung';