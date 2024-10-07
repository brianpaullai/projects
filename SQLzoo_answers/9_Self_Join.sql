-- 1.
SELECT COUNT(*)
FROM stops;

-- 2.
SELECT id
FROM stops
WHERE name = 'Craiglockhart';

-- 3.
SELECT id, name
FROM stops JOIN route ON stops.id = route.stop
WHERE num = '4'
AND company = 'LRT';

-- 4.
SELECT company, num, COUNT(*)
FROM route WHERE stop=149 OR stop=53
GROUP BY company, num
HAVING COUNT(*) = 2;

-- 5.
SELECT a.company, a.num, a.stop, b.stop
FROM route a JOIN route b ON (a.company=b.company AND a.num=b.num)
WHERE a.stop=53 
AND b.stop = 149;

-- 6.
SELECT a.company, a.num, stopa.name, stopb.name
FROM route a JOIN route b ON (a.company=b.company AND a.num=b.num)
     JOIN stops stopa ON (a.stop=stopa.id)
     JOIN stops stopb ON (b.stop=stopb.id)
WHERE stopa.name='Craiglockhart'
AND stopb.name = 'London Road';

-- 7.
SELECT DISTINCT a.company, a.num
FROM route a, route b
WHERE a.company=b.company 
AND a.num = b.num 
AND a.stop = 115 
AND b.stop = 137;

-- 8.
SELECT DISTINCT a.company, a.num
FROM route a, route b
WHERE a.company=b.company 
AND a.num = b.num 
AND a.stop = (SELECT id FROM stops WHERE name = 'Craiglockhart')
AND b.stop = (SELECT id FROM stops WHERE name = 'Tollcross');

-- 9.
SELECT DISTINCT S2.name, R2.company, R2.num
FROM stops S1, stops S2, route R1, route R2
WHERE S1.name = 'Craiglockhart'
  AND S1.id = R1.stop
  AND R1.company = R2.company 
  AND R1.num = R2.num
  AND R2.stop = S2.id;

-- 10.
