-- BOTTLENECK AND DOWNTIME ANALYSIS

alter table production_runs
alter column downtime_minutes int;

--1. which lines loses the most production time
select
	pl.line_id,
	pl.line_type,
	count(*) as total_runs,
	sum(pr.downtime_minutes) as total_downtime_minutes,
	round(avg(pr.downtime_minutes),2) as avg_downtime_per_run
from production_runs pr
join production_lines pl
on pr.line_id = pl.line_id
group by pl.line_id, pl.line_type
order by total_downtime_minutes desc;

-- 2.downtime as % of vailable time
select
	pr.line_id,
	pl.line_type,
	round(
		sum(pr.downtime_minutes) *1.0/
		nullif(sum(pr.run_hours * 60),0),3
		) as downtime_pct
from production_runs pr
join production_lines pl
on pr.line_id = pl.line_id
group by pr.line_id, pl.line_type
order by downtime_pct desc;

-- is downtime planned or breakdown driver?
select
	ml.line_id,
	pl.line_type,
	ml.maintenance_type,
	count(*) as incidents,
	sum(ml.downtime_minutes) as downtime_minutes
from maintenance_logs ml
join production_lines pl
on ml.line_id=pl.line_id
group by ml.line_id, pl.line_type, ml.maintenance_type
order by ml.line_id, downtime_minutes desc;

--utilization and downtime
with utilization AS (
	select
		pr.line_id,
		round(sum(pr.actual_units)*1.0 / nullif(sum(pl.max_units_per_hour*pr.run_hours),0)
		,3) as utilization_pct
	from production_runs pr
	join production_lines pl
	on pr.line_id=pl.line_id
	group by pr.line_id
),
downtime AS (
	Select
		line_id,
		round(sum(downtime_minutes)*1.0 / nullif(sum(run_hours*60),0),3) as downtime_pct
	from production_runs
	group by line_id
)
select
	u.line_id,
	u.utilization_pct,
	d.downtime_pct
from utilization u
join downtime d
on u.line_id = d.line_id
order by d.downtime_pct desc, u.utilization_pct asc;

-- production lost due to downtime
select
	pr.line_id,
	round(
		SUM(pr.downtime_minutes / 60.0 * pl.max_units_per_hour),0) as lost_units_estimate
from production_runs pr
join production_lines pl
	on pr.line_id=pl.line_id
group by pr.line_id
order by lost_units_estimate desc;