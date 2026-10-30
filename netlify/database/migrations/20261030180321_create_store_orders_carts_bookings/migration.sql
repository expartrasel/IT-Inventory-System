CREATE TABLE "service_bookings" (
	"id" text PRIMARY KEY,
	"name" text NOT NULL,
	"phone" text NOT NULL,
	"device" text NOT NULL,
	"problem" text NOT NULL,
	"date" text NOT NULL,
	"status" text DEFAULT 'requested' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "store_carts" (
	"id" text PRIMARY KEY,
	"items" jsonb DEFAULT '[]' NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "store_orders" (
	"id" text PRIMARY KEY,
	"session_id" text NOT NULL,
	"name" text NOT NULL,
	"phone" text NOT NULL,
	"email" text NOT NULL,
	"address" text NOT NULL,
	"items" jsonb NOT NULL,
	"total" integer NOT NULL,
	"delivery" integer NOT NULL,
	"payment_method" text NOT NULL,
	"payment_status" text DEFAULT 'unpaid' NOT NULL,
	"status" text DEFAULT 'received' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL
);
