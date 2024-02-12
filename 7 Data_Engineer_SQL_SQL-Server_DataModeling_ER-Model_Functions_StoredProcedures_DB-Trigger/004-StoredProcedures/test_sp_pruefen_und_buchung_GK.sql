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

EXEC [dbo].[sp_pruefungen_und_buchung] 
	3, -- KundenID 1 --> Hauptkunde und Zahler
	4, -- Optional KundenID2
	5, -- Optional KundenID3
	NULL, -- Optional KundenID3
	1,	-- ZimmmerID
	'2035-06-26', -- DatumVon
	'2035-06-28', -- DatumBis
	
	@Erfolg OUTPUT,
	@Feedback OUTPUT;


SELECT @Erfolg AS 'Geklappt?', @Feedback AS 'R�ckgabemeldung';
