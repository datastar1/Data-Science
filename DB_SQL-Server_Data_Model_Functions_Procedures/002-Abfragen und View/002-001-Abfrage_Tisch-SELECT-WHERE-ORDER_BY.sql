USE Hotel
GO

--Gibt es ein Tisch f�r 4 Person?

SELECT *
FROM tb_Tisch
WHERE SitzPlatz >= 4
ORDER BY SitzPlatz
