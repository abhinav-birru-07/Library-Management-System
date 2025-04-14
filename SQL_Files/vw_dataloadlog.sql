select * from temp.dataload;

select distinct factorname, details from temp.dataload where loadid in (123) and result='fail';

select * from temp.dataload where loadid in (123) and factorname='factor1';

select * from temp.dataload dl join 
(select distinct factorname as fl_factorname, valuedate as fl_valuedate, details as fl_details, loadid as fl_loadid 
from temp.dataload where loadid in (123) and result='fail') fl
on dl.loadid=fl.fl_loadid and dl.factorname=fl.fl_factorname and dl.valuedate=fl.fl_valuedate;


select factorname, valuedate, sum(case when result='success' then 1 else 0 end) as result_count
from (select * from temp.dataload dl join 
(select distinct factorname as fl_factorname, valuedate as fl_valuedate, details as fl_details, loadid as fl_loadid 
from temp.dataload where loadid in (123) and result='fail') fl
on dl.loadid=fl.fl_loadid and dl.factorname=fl.fl_factorname and dl.valuedate=fl.fl_valuedate) as join_table
group by factorname, valuedate;



