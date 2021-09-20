create table menu_items (
	"menu_id" serial NOT NULL PRIMARY KEY,
	"category" varchar(100) NOT NULL,
	"name" varchar(100) NOT NULL,
	"price" numeric(6, 2) NOT NULL
);

create table orders (
	"order_id" serial NOT NULL PRIMARY KEY,
	"total_price" numeric(6, 2) NOT NULL,
	"comments" text,
	"email" varchar(100)
);

create table ordered_items (
	"ordered_item_id" serial NOT NULL PRIMARY KEY,
	"menu_id" int NOT NULL,
	"order_id" int NOT NULL,
	"quantity" int NOT NULL,
	"unit_price" numeric(6, 2) NOT NULL,
	foreign key ("menu_id")
		references menu_items ("menu_id") on delete cascade,
	foreign key ("order_id")
		references orders ("order_id") on delete cascade
);
