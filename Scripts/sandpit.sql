
create schema sandpit;

create table sandpit.category_food as
select * from ods.category_food;

create table sandpit.diary_meal as
select * from ods.diary_meal;

create table sandpit.food as
select * from ods.food;

create table sandpit.ingredients as
select * from ods.ingredients;

create table sandpit.mealtime as
select * from ods.mealtime;

create table sandpit.recipe as
select * from ods.recipe;

create table sandpit.recipe_info as
select * from ods.recipe_info;

create table sandpit.recipe_post as
select * from ods.recipe_post;

create table sandpit.users as
select * from ods.users;