drop table if exists menu_items cascade; 
drop table if exists orders cascade; 
drop table if exists ordered_items cascade;

create table menu_items (
	"id" serial NOT NULL PRIMARY KEY,
	"category" varchar(100) NOT NULL,
	"name" varchar(100) NOT NULL,
	"price" numeric(6, 2) NOT NULL
);

create table orders (
	"id" serial NOT NULL PRIMARY KEY,
	"total_price" numeric(6, 2) NOT NULL,
	"comments" text,
	"email" varchar(100)
);

create table ordered_items (
	"id" serial NOT NULL PRIMARY KEY,
	"menu_item_id" int NOT NULL,
	"order_id" int NOT NULL,
	"quantity" int NOT NULL,
	"unit_price" numeric(6, 2) NOT NULL,
	foreign key ("menu_item_id")
		references menu_items ("id") on delete cascade,
	foreign key ("order_id")
		references orders ("id") on delete cascade
);

INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Margheritta', 'Pizza', 20);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Vegetariana', 'Pizza', 22);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Tosca', 'Pizza', 25);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Venecia', 'Pizza', 25);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Double Cheese', 'Pizza Addons', 2);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Salami', 'Pizza Addons', 2);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Ham', 'Pizza Addons', 2);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Mushrooms', 'Pizza Addons', 2);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Schnitzel', 'Main Dish', 30);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Fish and Chips', 'Main Dish', 28);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Hungarian Cake', 'Main Dish', 27);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Salads', 'Side Dish', 5);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Sauces', 'Side Dish', 6);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Tomato Soup', 'Soup', 12);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Chicken Soup', 'Soup', 10);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Coffee', 'Drinks', 5);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Tea', 'Drinks', 5);
INSERT INTO public."menu_items" ("name", "category", "price") VALUES ('Coke', 'Drinks', 5);
