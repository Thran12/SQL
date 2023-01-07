-- This sort of Sql queries are applied to a specific data source useful for tax information in USA

-- Joining of one table with another to get companies with similar match name as a result.The match rate should be vary from 30-70 percent

SELECT distinct * from (select distinct * from BGNOW
where Vendor_Name not in (select distinct Vendor_Name from (select * from BGNOW bg
inner join sec_5500_Charity_non_profit csc on bg.Vendor_Name=
SUBSTRING(Business_Name,1,LEN(bg.Vendor_Name))
where FEIN not in ('0','NULL'))t1))t1
inner join ein_master_38mm_deduplicated em on t1.Vendor_Name=
SUBSTRING(em.COMPANY,1,LEN(Vendor_Name))


-- deduplication using a special criteria in windows functions
select * into ein_master 
from (select * from (select *,Row_number() over(partition by fein,substring(Company,1,3)
,substring(Address,1,6) order by 
cast(Date_Reported as int
)desc) as R_ from 
(select distinct * from ein_master_database
where FEIN<>'0')t1
where FEIN <> 'NULL' and FEIN not in ('000000000','NOT APPLICABLE','APPLIED FOR'))t2
where R_=1)t7

--Cleaning up another file regarding tax data
select * from sec_5500_Charity_non_profit
where fein in (select distinct fein from 
(select * from (select *,ROW_NUMBER() over(partition by fein order by fein) as row__ from (select * from sec_5500_Charity_non_profit 
where FEIN not in ('0','NULL'))t1)t2
where row__>=2)t2)
order by FEIN



--   You cannot store data result from stored procedures into subquery or common table expressions so temporary tables are the best solution in such cases

create procedure brand_copiers @brand_name varchar(30)
as 
select * from 
(
select * from 
(select *,
ROW_NUMBER() over(partition by  Ucc1_filing_number,Ucc1_filing_number2,sec_name,deb_name,deb_address_line1
--SEC_name,sec_address_line1,deb_address_line1 
order by sec_address_line1) as ro_
from Copier_secureds_debters
where SEC_NAME like @brand_name )t1
where ro_=1
)t2
inner join filings_full ff on t2.UCC1_FILING_NUMBER=ff.UCC1_FILING_NUMBER_
where YEAR(FILING_DATE)>2014


DROP TABLE IF EXISTS #dT
CREATE TABLE #dT (
Ucc1_filing_number nvarchar(30),sec_name nvarchar (100),sec_name_format nvarchar(50),
sec_address_line1 nvarchar(100),sec_address_line2 nvarchar(100),sec_city nvarchar(50),
sec_state_province nvarchar(50),sec_zipcode nvarchar(50),sec_country nvarchar(50),sec_ref_number nvarchar(50),sec_rel_to_filing nvarchar(50),
sec_orig_party nvarchar(50),sec_filing_status nvarchar(50),Ucc1_filing_number2 nvarchar(30),
deb_name nvarchar (100),deb_name_format nvarchar(50),
deb_address_line1 nvarchar(100),deb_address_line2 nvarchar(100),deb_city nvarchar(50),
deb_state_province nvarchar(50),deb_zipcode nvarchar(50),deb_country nvarchar(50),deb_ref_number nvarchar(50),deb_rel_to_filing nvarchar(50),
deb_orig_party nvarchar(50),deb_filing_status nvarchar(50),ro_ int,UCc1_FILING_NUMBER_ nvarchar(100),
FILING_DATE nvarchar(50),FILING_pages nvarchar(50),FILING_TOT_pages nvarchar(50),FILING_STATUS nvarchar(50),
FILING_cancel_date nvarchar(50),filing_exp_date nvarchar(50),Filing_trans_util nvarchar(50),
filing_event_cnt nvarchar (50),Filing_tot_deb_cnt nvarchar(50),Filing_tot_sec_cnt nvarchar(50),filing_cur_deb_cnt nvarchar(50),
filing_cur_sec_cnt nvarchar(50))

INSERT #dT

exec brand_copiers @brand_name='%Konica%'
INSERT #dT
-- here the data is stored in temp table Dt..Although creation of temp table may seem hard but through this way you automate alot of your work for future use 

INSERT #dT
exec brand_copiers @brand_name='%Hewlett%'
INSERT #dT
exec brand_copiers @brand_name='%Pitney%'
INSERT #dT

--Another way to get same result as above  but there is no automation in this case


select * from (select * from (select * from (select * from 
(select *,YEAR(FILING_DATE) as Year_ from filings_full)t1
where Year_>=2015) as t2
inner join Copier_secureds_debters_events as csde on t2.UCC1_FILING_NUMBER_=
csde.UCC1_FILING_NUMBER)t3
where SEC_NAME like '%kyocera%' or sec_name like '%Xerox%' or sec_name like '%ricoh%' or 
SEC_NAME like '%canon%' or SEC_NAME like '%minolta%' or SEC_NAME like '%Lanier%' or 
sec_name like '%Toshiba%'
or SEC_NAME like '%Sharp%' or SEC_NAME like '%Pitney%' or SEC_NAME like '%Hewlett Packard%' 
or SEC_NAME like '%lexmark%'  or SEC_NAME like '%IBM%' or sec_name like
'%Kinica%')t5
where SEC_NAME not like '%BANK%' 
