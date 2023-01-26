BEGIN;

-- Oppgave 2a
SELECT * FROM planet WHERE stjerne = 'Proxima Centauri';

-- b
SELECT DISTINCT oppdaget FROM planet
WHERE stjerne = 'TRAPPIST-1' or stjerne = 'Kepler-154';

-- c
SELECT COUNT(*) FROM planet WHERE masse IS NULL;

-- d
SELECT * FROM planet
WHERE masse > (SELECT Avg(masse) FROM planet) and oppdaget = 2020;

-- e
SELECT MAX(oppdaget) - MIN(oppdaget) FROM planet;


-- Oppgave 3a
SELECT DISTINCT p.navn AS planet_navn
FROM planet p
INNER JOIN materie m ON p.navn=m.planet
WHERE 3 < masse and masse < 10 and molekyl = 'H2O';

-- b
SELECT DISTINCT p.navn AS planet_navn
FROM planet p
INNER JOIN materie m ON p.navn=m.planet
INNER JOIN stjerne s ON p.stjerne=s.navn
WHERE avstand < (s.masse * 12) and molekyl LIKE '%H%';

-- c
SELECT p.navn AS planet_navn
FROM planet p
WHERE masse > 10 and stjerne is not NULL;
INNER JOIN stjerne s ON p.stjerne=s.navn;
WHERE avstand < 50
GROUP BY s.navn
HAVING COUNT(*) >= 2;


/*
4
    Nils probably doesn't understand how JOINs work!
    A NATURAL JOIN requires columns with common values for;
    being very attractive to technicians it sadly doesn't work here!
    The navn column, being the only common column, are the names of two
    categorically different entities, planets and stars.

    We have to do an INNER JOIN where we explicitely couple
    planet.stjerne to the stjerne.navn as follows:
*/
SELECT oppdaget
FROM planet p
INNER JOIN stjerne s ON p.stjerne=s.navn;
WHERE avstand > 8000;

-- 5a
INSERT INTO stjerne
VALUES ('Sola', 0, 1);

-- b
INSERT INTO planet
VALUES ('Jorda', 0.003146, Null, 'Sola');

-- 6
CREATE TABLE observasjon (
    observasjons_id INT PRIMARY KEY,
    timestamp timestamp NOT NULL,
    planet text NOT NULL REFERENCES planet(navn),
    kommentar text
);
