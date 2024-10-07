-- 1.
SELECT yr, subject, winner
FROM nobel
WHERE yr = 1950;

-- 2.
SELECT winner
FROM nobel
WHERE yr = 1962
AND subject = 'literature';

-- 3.
SELECT yr, subject
FROM nobel
WHERE winner = 'Albert Einstein';

-- 4.
SELECT winner
FROM nobel
WHERE yr >= 2000
AND subject = 'peace';

-- 5.
SELECT yr, subject, winner
FROM nobel
WHERE yr >= 1980 
AND yr <= 1989
AND subject = 'literature';

-- 6.
SELECT * 
FROM nobel
WHERE winner IN ('Theodore Roosevelt', 'Woodrow Wilson', 'Jimmy Carter', 'Barack Obama');

-- 7.
SELECT winner 
FROM nobel
WHERE winner LIKE 'John%';

-- 8.
SELECT yr, subject, winner
FROM nobel
WHERE (yr = 1980 AND subject = 'physics')
OR (yr = 1984 AND subject = 'chemistry');

-- 9.
SELECT yr, subject, winner
FROM nobel
WHERE yr = 1980 AND (subject <> 'chemistry' AND subject <> 'medicine');

-- 10.
SELECT yr, subject, winner
FROM nobel
WHERE (yr < 1910 AND subject = 'medicine')
OR (yr >= 2004 AND subject = 'literature');

-- 11.
SELECT yr, subject, winner
FROM nobel
WHERE winner = 'PETER GRÜNBERG';

-- 12.
SELECT yr, subject, winner
FROM nobel
WHERE winner = "EUGENE O'NEILL";

-- 13.
SELECT winner, yr, subject
FROM nobel
WHERE winner LIKE 'Sir %';