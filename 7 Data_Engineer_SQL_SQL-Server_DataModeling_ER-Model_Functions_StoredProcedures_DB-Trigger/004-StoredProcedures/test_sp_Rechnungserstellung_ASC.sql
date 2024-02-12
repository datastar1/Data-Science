USE [HOTEL];
GO

DECLARE	@Erfolg bit; -- geklappt oder nicht
DECLARE	@Feedback VARCHAR(MAX); -- Fehlermeldungen etc.

EXEC [dbo].[sp_Rechnungserstellung_ASC]
	2,	-- ZimmmerID
	
	
	@Erfolg OUTPUT,
	@Feedback OUTPUT;


SELECT @Erfolg AS 'Geklappt?', @Feedback AS 'Rückgabemeldung';