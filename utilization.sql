-- BASE DATASET FOR CAPACITY UTILIZATION
SELECT
	pr.date,
	pr.plant_id,
	pr.line_id,
	pr.shift_id,
	pl.line_type,
	sh.shift_name,
	pl.max_units_per_hour,
	pr.run_hours,
	pr.actual_units,
	(pl.max_units_per_hour * pr.run_hours) as theoretical_capacity_units
From production_runs pr
join production_lines pl
	on pr.line_id = pl.line_id
join shifts sh
	on pr.shift_id = sh.shift_id

-- CAPACITY UTILIZATION BY LINE AND SHIFT
select 
	date,
	plant_id,
	line_id,
	shift_id,
	shift_name,
	round(sum(actual_units)*1.0 / nullif(sum(max_units_per_hour*run_hours),0),3) as capacity_utilization_pct
FROM(
	SELECT
	pr.date,
	pr.plant_id,
	pr.line_id,
	pr.shift_id,
	pl.line_type,
	sh.shift_name,
	pl.max_units_per_hour,
	pr.run_hours,
	pr.actual_units,
	(pl.max_units_per_hour * pr.run_hours) as theoretical_capacity_units
From production_runs pr
join production_lines pl
	on pr.line_id = pl.line_id
join shifts sh
	on pr.shift_id = sh.shift_id
) base
group by 
	date, plant_id, line_id, shift_id, shift_name
order by
	date, plant_id, shift_id

-- CAPACITY UTILIZATION BY LINE(MONTHLY VIEW)
SELECT
	DATEPART(YEAR,pr.date) as YEAR,
	DATEPART(Month,pr.date) as month,
	pl.plant_id,
	pl.line_id,
	round(sum(pr.actual_units)*1.0 / nullif(sum(pl.max_units_per_hour * pr.run_hours),0),3) as capacity_utilization_pct
from production_runs pr
join production_lines pl
on pr.line_id = pl.line_id
group by
	DATEPART(YEAR,pr.date),
	DATEPART(Month,pr.date),
	pl.plant_id,
	pl.line_id
order by
	year, month, plant_id, line_id;

-- CAPACITY UTILIZATION BY PLANT
Select
	DATEPART(year,pr.date) as year,
	DATEPART(month,pr.date) as month,
	pl.plant_id,
	round(sum(pr.actual_units)*1.0/nullif(sum(pl.max_units_per_hour*pr.run_hours),0),3) as plant_capacity_utilization_pct
from production_runs pr
join production_lines pl
on pr.line_id=pl.line_id
group by DATEPART(year,pr.date), DATEPART(Month,pr.date),pl.plant_id
order by year,month, pl.plant_id

--SANITY CHECK, rows should be zero
select *
from(
	select
	pr.run_id,
	pr.actual_units,
	pl.max_units_per_hour * pr.run_hours as theoretical_capacity
from production_runs pr
join production_lines pl 
on pr.line_id = pl.line_id
) t
where actual_units > theoretical_capacity;