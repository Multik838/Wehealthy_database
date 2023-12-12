
create table cdm.analysis_report as
select 
odm.report_date,
ou.user_id,ou.gender,ou.user_age,ou.weight_kg,ou.height_cm,
odm.mealtime_id, odm.food_id,odm.food_category_ncode, 
case when orp.meal_link is not null then true else false end as activity,
f.food_calories, f.food_proteins,f.food_fats,f.food_carbon 
FROM ods.users as ou
JOIN ods.diary_meal as odm on 
ou.user_id = odm.user_id
left join ods.recipe_post as orp on 
ou.user_id = orp.user_id and 
odm.report_date = orp.report_date
join ods.food as f on 
odm.food_id = f.food_id and
odm.food_category_ncode = f.food_category_ncode;


select * from cdm.analysis_report