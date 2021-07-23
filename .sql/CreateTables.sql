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
		references Menu ("MenuID"),
	foreign key ("OrderID")
		references Orders ("OrderID")
);
