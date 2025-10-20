CREATE TABLE "transactions" (
	"id"	INTEGER NOT NULL,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"currency_from"	TEXT NOT NULL,
	"amount_from"	REAL NOT NULL,
	"currency_to"	TEXT NOT NULL,
	"amount_to"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);