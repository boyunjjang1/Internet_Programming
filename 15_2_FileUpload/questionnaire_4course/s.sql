SELECT COUNT(*) as student_total,
SUM( CASE WHEN use_flag='Y' THEN 1 ELSE 0 END ) as student_y_cnt, 
SUM( CASE WHEN use_flag='N' THEN 1 ELSE 0 END ) as student_n_cnt, 
SUM( CASE WHEN q1='Y' THEN 1 ELSE 0 END ) as q1_y, 
SUM( CASE WHEN q1='N' THEN 1 ELSE 0 END ) as q1_n, 
SUM( CASE WHEN q1 is null THEN 1 ELSE 0 END ) as q1_null, 
SUM( CASE WHEN q2='1' THEN 1 ELSE 0 END ) as q2_1, 
SUM( CASE WHEN q2='2' THEN 1 ELSE 0 END ) as q2_2, 
SUM( CASE WHEN q2='3' THEN 1 ELSE 0 END ) as q2_3, 
SUM( CASE WHEN q2 is null THEN 1 ELSE 0 END ) as q2_null
FROM tbQ;