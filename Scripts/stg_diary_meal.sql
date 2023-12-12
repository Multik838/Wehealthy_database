-- stg.category_food определение

-- Drop table

-- DROP TABLE stg.category_food;

CREATE TABLE stg.category_food (
	food_category_id bigserial NOT NULL,
	food_category_ncode int4 NOT NULL,
	food_category_name varchar(255) NOT NULL,
	CONSTRAINT category_food_pkey PRIMARY KEY (food_category_id)
);


-- stg.diary_meal определение

-- Drop table

-- DROP TABLE stg.diary_meal;

CREATE TABLE stg.diary_meal (
	unique_key text NOT NULL,
	user_id int8 NULL,
	mealtime_id int4 NULL,
	food_id int4 NULL,
	food_category_ncode int4 NULL,
	report_date date NULL,
	CONSTRAINT diary_meal_pkey PRIMARY KEY (unique_key)
);


-- stg.food определение

-- Drop table

-- DROP TABLE stg.food;

CREATE TABLE stg.food (
	food_id bigserial NOT NULL,
	food_category_ncode int4 NULL,
	food_name text NULL,
	food_calories float8 NULL,
	food_proteins float8 NULL,
	food_fats float8 NULL,
	food_carbon float8 NULL,
	CONSTRAINT food_pkey PRIMARY KEY (food_id)
);


-- stg.ingredients определение

-- Drop table

-- DROP TABLE stg.ingredients;

CREATE TABLE stg.ingredients (
	meal_key varchar NULL,
	meal_name varchar NULL,
	meal_ingredient varchar NULL,
	meal_quantity varchar NULL,
	meal_link text NULL
);



-- stg.recipe определение

-- Drop table

-- DROP TABLE stg.recipe;

CREATE TABLE stg.recipe (
	meal_key varchar NULL,
	recipe_description text NULL
);


-- stg.recipe_info определение

-- Drop table

-- DROP TABLE stg.recipe_info;

CREATE TABLE stg.recipe_info (
	unique_key bigserial NOT NULL,
	user_id int8 NULL,
	meal_name text NULL,
	report_date date NULL,
	CONSTRAINT recipe_info_pkey PRIMARY KEY (unique_key)
);


-- stg.users определение

-- Drop table

-- DROP TABLE stg.users;

CREATE TABLE stg.users (
	user_id bigserial NOT NULL,
	gender varchar(3) NOT NULL,
	user_age int4 NOT NULL,
	weight_kg int4 NULL,
	height_cm int4 NULL,
	CONSTRAINT user_pkey PRIMARY KEY (user_id)
);
