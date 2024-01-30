USE Hotel
GO

--Gibt es ein Tisch für 4 Person?

SELECT *
FROM tb_Tisch
WHERE SitzPlatz >= 4
ORDER BY SitzPlatz
