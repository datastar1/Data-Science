USE [HOTEL]
GO

--***Prozess Workflow***
-- Anruf:
-- Zimmer für 2 Personen
-- Zeitraum: xyz

--Rezeptionist fragt freie Zimmer im System ab

-- Übergabe der Personenzahl für die ein Zimmer gesucht wird
SELECT * 
FROM tf_passende_Zimmer(2);


-- Rezeptionist teilt die möglichen freien Zimmer mit inkl. Preis und Kategorie
-- Kunde entscheidet sich für bestimmte Kategorie und möchte buchen
-- Rezeptionist definiert auf den Kundenangaben passendes Zimmer (ZimmerID) und führt die Buchung durch sofern das Zimmer im Zeitraum verfügbar ist


DECLARE	@Erfolg bit; -- geklappt oder nicht
DECLARE	@Feedback VARCHAR(MAX); -- Fehlermeldungen etc.

EXEC [dbo].[sp_AnlageBuchung_ASC]
	2,	-- ZimmmerID
	'2034-01-11', -- DatumVon
	'2034-01-12', -- DatumBis
	3, -- KundenID 1 --> Hauptkunde und Zahler
	NULL, -- Optional KundenID2
	NULL, -- Optional KundenID3
	4, -- Optional KundenID4
	
	
	@Erfolg OUTPUT,
	@Feedback OUTPUT;


SELECT @Erfolg AS 'Geklappt?', @Feedback AS 'Rückgabemeldung';
