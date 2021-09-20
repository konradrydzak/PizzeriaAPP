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