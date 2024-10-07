-- 1.
SELECT id, title
FROM movie
WHERE yr=1962;

-- 2.
SELECT yr
FROM movie
WHERE title = 'Citizen Kane';

-- 3.
SELECT id, title, yr
FROM movie
WHERE title LIKE '%Star Trek%'
ORDER BY yr;

-- 4.
SELECT id
FROM actor
WHERE name = 'Glenn Close';

-- 5.
SELECT id
FROM movie
WHERE title = 'Casablanca';

-- 6.
SELECT name
FROM casting JOIN actor ON actorid = id
WHERE movieid = 11768;

-- 7.
SELECT name
FROM casting JOIN actor ON actorid = id
WHERE movieid = (SELECT id FROM movie WHERE title = 'Alien');

-- 8.
SELECT title
FROM movie JOIN casting ON id = movieid
WHERE actorid = (SELECT id FROM actor WHERE name = 'Harrison Ford');

-- 9.
SELECT title
FROM movie JOIN casting ON id = movieid
WHERE actorid = (SELECT id FROM actor WHERE name = 'Harrison Ford')
AND ord <> 1;

-- 10.
SELECT title, name
FROM (movie JOIN casting ON movie.id = movieid) JOIN actor ON actorid = actor.id 
WHERE ord = 1 AND yr = 1962;

-- 11.
SELECT yr,COUNT(title) FROM
movie JOIN casting ON movie.id=movieid JOIN actor ON actorid=actor.id
WHERE name='Rock Hudson'
GROUP BY yr
HAVING COUNT(title) > 2;

-- 12.
SELECT title, name
FROM (movie JOIN casting ON movie.id = movieid) JOIN actor ON actorid = actor.id 
WHERE movie.id IN (SELECT movieid FROM casting
                    WHERE actorid IN (SELECT id FROM actor
                                      WHERE name='Julie Andrews'))
AND ord = 1;

-- 13.
SELECT DISTINCT name FROM casting JOIN actor ON actorid = id
WHERE actorid IN (SELECT actorid FROM casting
                  WHERE ord=1
                  GROUP BY actorid
                  HAVING COUNT(actorid)>=15)
ORDER BY name;

-- 14.
SELECT title, COUNT(actorid) FROM movie JOIN casting ON movieid = id
WHERE yr = 1978
GROUP by title
ORDER BY COUNT(actorid) DESC, title;

-- 15.
SELECT name from casting JOIN actor ON actorid = id
WHERE name <> 'Art Garfunkel' 
AND movieid IN (SELECT movieid from actor JOIN casting on id = actorid
                WHERE name = 'Art Garfunkel');