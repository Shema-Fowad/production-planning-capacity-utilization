--SHIFT PRODUCTIVITY AND LABOR EFFICIENCY
-- 1. output per hour by shift
-- output/hour = total actual units/total run hours
select
	sh.shift_name,
	round(sum(pr.actual_units)*1.0 / nullif(sum(pr.run_hours),0),2) as units_per_hour
from production_runs pr
join shifts sh
on sh.shift_id=pr.shift_id
group by sh.shift_name
order by units_per_hour desc;

--2. capacity utilization by shift
select 
	sh.shift_name,
	round(sum(pr.actual_units)*1.0/nullif(sum(pl.max_units_per_hour * pr.run_hours),0)
	,3) as shift_utilization_pct
from production_runs pr
join production_lines pl
	on pr.line_id=pl.line_id
join shifts sh
	on sh.shift_id=pr.shift_id
group by sh.shift_name
order by shift_utilization_pct desc;

--3. labor cost per unit by shift
-- labor cost per unit = (total run hours * labor cost per hour) / actual units

select
	sh.shift_name,
	round(
	sum(pr.run_hours * sh.labor_cost_per_hour) /
	nullif(sum(pr.actual_units),0),2) as labor_cost_per_unit
from production_runs pr
join shifts sh
	on sh.shift_id=pr.shift_id
group by sh.shift_name
order by labor_cost_per_unit;