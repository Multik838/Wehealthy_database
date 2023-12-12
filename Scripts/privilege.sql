-- Гранты для админа

GRANT ALL ON schema ods TO pgadmin;
grant all on table ods.food to pgadmin;
grant all on table ods.category_food to pgadmin;
grant all on table ods.users to pgadmin;
grant all on table ods.diary_meal to pgadmin;
grant all on table ods.recipe to pgadmin;
grant all on table ods.ingredients to pgadmin;
grant all on table ods.recipe_info to pgadmin;
grant all on table ods.recipe_post to pgadmin;
grant all on table ods.mealtime to pgadmin;


GRANT ALL ON schema sandpit TO pgadmin;
grant all on table sandpit.food to pgadmin;
grant all on table sandpit.category_food to pgadmin;
grant all on table sandpit.users to pgadmin;
grant all on table sandpit.diary_meal to pgadmin;
grant all on table sandpit.recipe to pgadmin;
grant all on table sandpit.ingredients to pgadmin;
grant all on table sandpit.recipe_info to pgadmin;
grant all on table sandpit.recipe_post to pgadmin;
grant all on table sandpit.mealtime to pgadmin;


-- Гранты для аналитика
GRANT select, create, TEMPORARY ON schema ods TO pganalytic;
grant SELECT on table ods.food to pganalytic;
grant SELECT on table ods.category_food to pganalytic;
grant SELECT on table ods.users to pganalytic;
grant SELECT on table ods.diary_meal to pganalytic;
grant SELECT on table ods.recipe to pgadmin;
grant SELECT on table ods.ingredients to pganalytic;
grant SELECT on table ods.recipe_info to pganalytic;
grant SELECT on table ods.recipe_post to pganalytic;
grant SELECT on table ods.mealtime to pganalytic;


-- Гранты для аналитика в песочнице
GRANT select, create, TEMPORARY ON schema sandpit TO pganalytic;
grant select, insert, update, delete, truncate, references on table sandpit.food to pganalytic;
grant select, insert, update, delete, truncate, references on tablesandpit.category_food to pganalytic;
grant select, insert, update, delete, truncate, references on table sandpit.users to pganalytic;
grant select, insert, update, delete, truncate, references on table sandpit.diary_meal to pganalytic;
grant select, insert, update, delete, truncate, references on table sandpit.recipe to pgadmin;
grant select, insert, update, delete, truncate, references on table sandpit.ingredients to pganalytic;
grant select, insert, update, delete, truncate, references on table sandpit.recipe_info to pganalytic;
grant select, insert, update, delete, truncate, references on table sandpit.recipe_post to pganalytic;
grant select, insert, update, delete, truncate, references on table sandpit.mealtime to pganalytic;


-- Гранты для бэкенда
GRANT select, create, TEMPORARY ON schema stg TO pgbackend;
grant SELECT on table stg.food to pgbackend;
grant SELECT on table stg.category_food to pgbackend;
grant SELECT on table stg.users to pgbackend;
grant SELECT on table stg.diary_meal to pgbackend;
grant SELECT on table stg.recipe to pgbackend;
grant SELECT on table stg.ingredients to pgbackend;
grant SELECT on table stg.recipe_info to pgbackend;