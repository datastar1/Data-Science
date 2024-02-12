USE [HOTEL]
GO

--***Prozess Workflow***
-- Anruf:
-- Zimmer f�r 2 Personen
-- Zeitraum: xyz

--Rezeptionist fragt freie Zimmer im System ab

-- �bergabe der Personenzahl f�r die ein Zimmer gesucht wird
SELECT * 
FROM tf_passende_Zimmer(2);


-- Rezeptionist teilt die m�glichen freien Zimmer mit inkl. Preis und Kategorie
-- Kunde entscheidet sich f�r bestimmte Kategorie und m�chte buchen
-- Rezeptionist definiert auf den Kundenangaben passendes Zimmer (ZimmerID) und f�hrt die Buchung durch sofern das Zimmer im Zeitraum verf�gbar ist


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


SELECT @Erfolg AS 'Geklappt?', @Feedback AS 'R�ckgabemeldung';
