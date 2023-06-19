CREATE TEMP TABLE IF NOT EXISTS _Variables(Name TEXT PRIMARY KEY, IntegerValue INTEGER);
-- INSERT INTO _Variables ( name ) VALUES ('VariableName2' );
-- UPDATE _Variables SET [IntegerValue] = 2 WHERE Name ='VariableName' ;
-- UPDATE _Variables SET [IntegerValue] = (SELECT COUNT(*) AS nums FROM urls ) WHERE Name ='VariableName9' ;

-- SELECT COUNT(*) as num FROM urls;
INSERT OR REPLACE INTO _Variables VALUES 
('allentry',
(SELECT COUNT(*) FROM urls )
);

INSERT OR REPLACE INTO _Variables VALUES 
('nothttp',
(SELECT COUNT(*) FROM urls WHERE url NOT LIKE 'http%')
);
DELETE FROM urls WHERE url NOT LIKE 'http%';

INSERT OR REPLACE INTO _Variables VALUES 
('count=0',
(SELECT COUNT(*) FROM urls WHERE visit_count = 0)
);
DELETE FROM urls WHERE visit_count = 0;

INSERT OR REPLACE INTO _Variables VALUES 
('visitime<',
(SELECT COUNT(*) FROM urls 
WHERE last_visit_time < (SELECT min(visit_time) FROM visits)-10 )
);
DELETE FROM urls 
WHERE last_visit_time < (SELECT min(visit_time) FROM visits)-10 ;

INSERT OR REPLACE INTO _Variables VALUES 
('baidu',
(SELECT COUNT(*) FROM urls WHERE url LIKE '%baidu%' ) 
);
DELETE FROM urls 
WHERE url LIKE '%baidu%' ;

INSERT OR REPLACE INTO _Variables VALUES 
('endentry',
(SELECT COUNT(*) FROM urls )
);

-----------------------------

INSERT OR REPLACE INTO _Variables VALUES
('visits',
( SELECT COUNT(*) FROM visits WHERE url NOT in (SELECT id FROM urls) )
);
DELETE FROM visits WHERE url NOT in (SELECT id FROM urls) ;

INSERT OR REPLACE INTO _Variables VALUES
('search',
( SELECT COUNT(*) FROM keyword_search_terms WHERE url_id NOT in (SELECT id FROM urls) )
);
DELETE FROM keyword_search_terms WHERE url_id NOT in (SELECT id FROM urls) ;

INSERT OR REPLACE INTO _Variables VALUES
('segment',
( SELECT COUNT(*) FROM segments WHERE url_id NOT in (SELECT id FROM urls) )
);
DELETE FROM segments WHERE url_id NOT in (SELECT id FROM urls) ;

INSERT OR REPLACE INTO _Variables VALUES
('segusage',
( SELECT COUNT(*) FROM segment_usage WHERE segment_id NOT in (SELECT id FROM segments) )
);
DELETE FROM segment_usage WHERE segment_id NOT in (SELECT id FROM segments) ;

-----------------------------------------
SELECT * FROM _Variables
-- SELECT id,url FROM urls
VACUUM;

-- SELECT COUNT(*) FROM urls 
-- WHERE last_visit_time <(SELECT min(visit_time) FROM visits)
-- AND url LIKE '%baidu%';

-- SELECT DISTINCT keyword_id FROM keyword_search_terms;
-- datetime("visit_time" / 1000000 - 11644473600 + 28800, 'unixepoch')