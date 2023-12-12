-- ods.food определение

-- Drop table

-- DROP TABLE ods.food;

CREATE TABLE ods.food (
  food_id bigserial NOT NULL,
  food_category_ncode int4 NULL,
  food_name text NULL,
  food_calories float8 NULL,
  food_proteins float8 NULL,
  food_fats float8 NULL,
  food_carbon float8 NULL,
  CONSTRAINT food_pkey PRIMARY KEY (food_id,food_category_ncode)
);

insert into ods.food
select * from stg.food;

select * from ods.food

-- ods.category_food определение

-- Drop table

-- DROP TABLE ods.category_food;

CREATE TABLE ods.category_food (
	food_category_id bigserial NOT NULL,
	food_category_ncode int4 NOT NULL,
	food_category_name varchar(255) NOT NULL,
	food_id bigint not null,
	CONSTRAINT category_food_pkey PRIMARY KEY (food_id)
);

insert into ods.category_food
select scf.food_category_id,scf.food_category_ncode,scf.food_category_name,sf.food_id from stg.category_food as scf
join stg.food as sf on
scf.food_category_ncode = sf.food_category_ncode
group by scf.food_category_id,scf.food_category_ncode,scf.food_category_name,sf.food_id;

alter table ods.category_food add constraint category_food_fkey FOREIGN KEY (food_id) REFERENCES ods.food(food_id) ON UPDATE cascade;

-- ods.users определение

-- Drop table

-- DROP TABLE ods.users;

CREATE TABLE ods.users (
	user_id bigserial NOT NULL,
	gender varchar(3) NOT NULL,
	user_age int4 NOT NULL,
	weight_kg int4 NULL,
	height_cm int4 NULL,
	CONSTRAINT user_pkey PRIMARY KEY (user_id)
);

insert into ods.users
select * from stg.users;

-- ods.diary_meal определение

-- Drop table

-- DROP TABLE ods.diary_meal;

CREATE TABLE ods.diary_meal (
	unique_key text NOT NULL,
	user_id int8 NULL,
	mealtime_id int4 NULL,
	food_id int4 null,
	food_category_ncode int4 NULL,
	report_date date NULL,
--	flag_new_food boolean not null,
	CONSTRAINT diary_meal_pkey PRIMARY KEY (unique_key, user_id, food_id, food_category_ncode,report_date),
	CONSTRAINT diary_users_fkey FOREIGN KEY (user_id) REFERENCES ods.users(user_id) ON UPDATE cascade,
	CONSTRAINT diary_mealtime_fkey FOREIGN KEY (mealtime_id) REFERENCES ods.mealtime(mealtime_id) ON UPDATE cascade,
	CONSTRAINT diary_food_fkey FOREIGN KEY (food_id) REFERENCES ods.food(food_id) ON UPDATE cascade
);


insert into ods.diary_meal
select * from stg.diary_meal;

-- ods.recipe определение

-- Drop table

-- DROP TABLE ods.recipe;

CREATE TABLE ods.recipe (
	meal_key varchar NULL,
	recipe_description text null,
	CONSTRAINT recipe_pkey PRIMARY KEY (meal_key)
);


insert into ods.recipe
select * from stg.recipe;

-- ods.ingredients определение

-- Drop table

-- DROP TABLE ods.ingredients;

CREATE TABLE ods.ingredients (
	meal_key varchar NULL,
	meal_name varchar NULL,
	meal_ingredient varchar NULL,
	meal_quantity varchar NULL,
	meal_link text null,
	CONSTRAINT meal_key_pkey PRIMARY KEY (meal_key, meal_ingredient,meal_quantity),
	CONSTRAINT recipe_fkey FOREIGN KEY (meal_key) REFERENCES ods.recipe(meal_key)
);

insert into ods.ingredients
select meal_key,meal_name,meal_ingredient,meal_quantity,meal_link from stg.ingredients
group by meal_key,meal_name,meal_ingredient,meal_quantity,meal_link;

-- ods.recipe_info определение

-- Drop table

-- DROP TABLE ods.recipe_info;

CREATE TABLE ods.recipe_info (
	unique_key bigserial NOT NULL,
	user_id int8 NULL,
	meal_name text NULL,
	report_date date NULL,
	CONSTRAINT recipe_info_pkey PRIMARY KEY (unique_key),
	CONSTRAINT recipe_info_users_fkey FOREIGN KEY (user_id) REFERENCES ods.users(user_id) ON UPDATE CASCADE
);

insert into ods.recipe_info
select * from stg.recipe_info;

-- ods.recipe_post определение

-- Drop table

-- DROP TABLE ods.recipe_post;

CREATE TABLE ods.recipe_post (
	user_id int8 NULL,
	meal_key varchar NULL,
	meal_link text NULL,
	report_date date null,
	CONSTRAINT recipe_post_pkey PRIMARY KEY (meal_key),
	CONSTRAINT recipe_post_users_fkey FOREIGN KEY (user_id) REFERENCES ods.users(user_id) ON UPDATE cascade,
	CONSTRAINT recipe_post_ingredients_fkey FOREIGN KEY (meal_key) REFERENCES ods.ingredients(meal_key) ON UPDATE CASCADE
);



with new_post as (
select 
row_number() over(partition by ori.user_id, oi.meal_key order by ori.report_date DESC) as rn,
ori.user_id,oi.meal_key,oi.meal_link,ori.report_date from ods.recipe_info as ori
join ods.ingredients as oi on 
ori.meal_name = oi.meal_name
group by ori.user_id,oi.meal_key,oi.meal_link,ori.report_date)
insert into ods.recipe_post 
select user_id,meal_key,meal_link,report_date
from new_post;


drop table ods.mealtime;

create table ods.mealtime (
mealtime varchar(20),
mealtime_id int,
CONSTRAINT mealtime_id_pkey PRIMARY KEY (mealtime_id)
);

delete from ods.mealtime;
insert into ods.mealtime (mealtime, mealtime_id) values 
('Завтрак',1),
('Ланч',2),
('обед',3),
('полдник',4),
('ужин',5),
('поздний ужин',6);

alter table ods.diary_meal add CONSTRAINT mealtime_id_diary_fkey FOREIGN KEY (mealtime_id) REFERENCES ods.mealtime(mealtime_id) ON UPDATE cascade;


alter table ods.recipe_post add CONSTRAINT recipe_post_meal_key_fkey FOREIGN KEY (meal_key) REFERENCES ods.recipe(meal_key);


