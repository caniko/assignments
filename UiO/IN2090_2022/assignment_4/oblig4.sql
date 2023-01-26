-- Question 1

SELECT concat(p.firstname, ' ', p.lastname), c.filmcharacter
FROM filmparticipation AS a INNER JOIN film as f
    ON (a.filmid = f.filmid)
INNER JOIN person as p
    ON (a.personid = p.personid)
INNER JOIN filmcharacter AS c
    ON (a.partid = c.partid)
WHERE f.title = 'Star Wars';

-- Question 2

SELECT country, count(filmid)
FROM filmcountry
GROUP BY country;

-- Question 3

SELECT i.country, avg(i.cast_time)
FROM (
    SELECT c.country, CASE WHEN t.time ~ '^\d+$' THEN CAST(t.time AS DOUBLE PRECISION) END AS cast_time
    FROM filmcountry AS c
    INNER JOIN runningtime AS t
        ON (c.filmid = t.filmid)
) AS i
GROUP BY i.country
HAVING count(i.cast_time) >= 200;

-- Question 4

SELECT f.title, count(g.genre) FROM filmgenre AS g
INNER JOIN film AS f
    ON (g.filmid = f.filmid)
GROUP BY f.title
ORDER BY count(g.genre) DESC, f.title ASC
LIMIT 10;

-- Question 5

SELECT c.country, count(c.country), avg(r.rank) AS avg_rating, mode() within group (order by g.genre) AS common_genre
FROM filmgenre AS g
INNER JOIN filmcountry AS c
    ON (g.filmid = c.filmid)
INNER JOIN filmrating AS r
    ON (c.filmid = r.filmid)
GROUP BY c.country;

-- Question 6

WITH
    p2f AS (
        SELECT personid, filmid FROM filmparticipation
            INNER JOIN filmcountry as c USING (filmid)
        WHERE c.country = 'Norway'
    ),
    fp2f AS (
        SELECT concat(p.firstname, ' ', p.lastname) AS name, p2f.filmid FROM p2f
            INNER JOIN person AS p USING (personid)
    ),
    pairs AS (
        SELECT DISTINCT fp2f_i.name AS name_i, fp2f_ii.name AS name_ii
        FROM fp2f AS fp2f_i
            INNER JOIN fp2f AS fp2f_ii USING (filmid)
        WHERE fp2f_i.name > fp2f_ii.name
        GROUP BY fp2f_i.name, fp2f_ii.name
        HAVING count(fp2f_i.filmid) >= 40
    )
SELECT * FROM pairs;

-- Question 7

SELECT f.title, f.prodyear FROM film AS f
    INNER JOIN filmgenre as g USING (filmid)
    INNER JOIN filmcountry as c USING (filmid)
WHERE (
    LOWER(f.title) LIKE '%dark%'
    OR LOWER(f.title) LIKE '%night%'
    AND g.genre = 'Horror'
    OR c.country = 'Romania'
);

-- Question 8

SELECT f.title, count(fp.personid)
FROM filmparticipation AS fp
    LEFT JOIN film as f USING (filmid)
WHERE f.prodyear >= 2010
GROUP BY f.title
HAVING count(fp.personid) <= 2;

-- Question 9

SELECT i.filmid FROM filmgenre AS i
    INNER JOIN filmgenre AS ii ON (i.filmid = ii.filmid)
WHERE i.genre > ii.genre AND i.genre != 'Sci-Fi' AND i.genre != 'Horror' AND ii.genre != 'Sci-Fi' AND ii.genre != 'Horror'
GROUP BY i.filmid;

-- Question 10

WITH
    r AS (
        SELECT filmid FROM filmrating
        r.rank >= 8.0 AND r.votes >= 1000
        LIMIT 10
    ),
    f AS (
        SELECT filmid FROM film
        WHERE firstname = 'Harrison' AND lastname = 'Ford'
    ),
    g AS (
        SELECT filmid FROM filmgenre
        WHERE genre = 'Comedy' OR genre = 'Romance'
    )
SELECT f.title, count(l.language) FROM r
    LEFT JOIN f ON

SELECT f.title, count(l.language)
FROM filmrating AS r
    INNER JOIN filmparticipation as fp ON (r.filmid = fp.filmid)
    INNER JOIN person as p ON (fp.personid = p.personid)
    INNER JOIN filmgenre as g ON (r.filmid = g.filmid)
    INNER JOIN film as f ON (r.filmid = f.filmid)
    LEFT JOIN filmlanguage as l ON (r.filmid = l.filmid)
WHERE (r.rank >= 8.0 AND r.votes >= 1000) AND ((p.firstname = 'Harrison' AND p.lastname = 'Ford') OR (g.genre = 'Comedy' OR g.genre = 'Romance'))
GROUP BY f.title;
