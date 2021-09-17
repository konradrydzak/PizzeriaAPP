drop table if exists menu cascade; 
drop table if exists orders cascade; 
drop table if exists ordereditems cascade; 

create table menu (
	"MenuID" serial NOT NULL PRIMARY KEY,
	"Category" varchar(100) NOT NULL,
	"Name" varchar(100) NOT NULL,
	"Price" numeric(6, 2) NOT NULL
);

create table orders (
	"OrderID" serial NOT NULL PRIMARY KEY,
	"TotalPrice" numeric(6, 2) NOT NULL,
	"Comments" text,
	"Email" varchar(100)
);

create table orderedItems (
	"OrderedItemID" serial NOT NULL PRIMARY KEY,
	"MenuID" int NOT NULL,
	"OrderID" int NOT NULL,
	"Quantity" int NOT NULL,
	"UnitPrice" numeric(6, 2) NOT NULL,
	foreign key ("MenuID")
		references Menu ("MenuID") on delete cascade,
	foreign key ("OrderID")
		references Orders ("OrderID") on delete cascade
);

INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Margheritta', 'Pizza', 20);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Vegetariana', 'Pizza', 22);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Tosca', 'Pizza', 25);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Venecia', 'Pizza', 25);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Double Cheese', 'Pizza Addons', 2);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Salami', 'Pizza Addons', 2);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Ham', 'Pizza Addons', 2);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Mushrooms', 'Pizza Addons', 2);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Schnitzel', 'Main Dish', 30);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Fish and Chips', 'Main Dish', 28);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Hungarian Cake', 'Main Dish', 27);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Salads', 'Side Dish', 5);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Sauces', 'Side Dish', 6);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Tomato Soup', 'Soup', 12);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Chicken Soup', 'Soup', 10);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Coffee', 'Drinks', 5);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Tea', 'Drinks', 5);
INSERT INTO public."menu" ("Name", "Category", "Price") VALUES ('Coke', 'Drinks', 5);
