import { pgTable, text, timestamp, integer, jsonb } from 'drizzle-orm/pg-core';
export const carts = pgTable('store_carts', {
  id: text().primaryKey(),
  items: jsonb().$type<{id: string; quantity: number}[]>().notNull().default([]),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});
export const orders = pgTable('store_orders', {
  id: text().primaryKey(), sessionId: text('session_id').notNull(),
  name: text().notNull(), phone: text().notNull(), email: text().notNull(), address: text().notNull(),
  items: jsonb().$type<{id: string; name: string; price: number; quantity: number}[]>().notNull(),
  total: integer().notNull(), delivery: integer().notNull(),
  paymentMethod: text('payment_method').notNull(), paymentStatus: text('payment_status').notNull().default('unpaid'),
  status: text().notNull().default('received'), createdAt: timestamp('created_at').notNull().defaultNow(),
});
export const bookings = pgTable('service_bookings', {
  id: text().primaryKey(), name: text().notNull(), phone: text().notNull(),
  device: text().notNull(), problem: text().notNull(), date: text().notNull(),
  status: text().notNull().default('requested'), createdAt: timestamp('created_at').notNull().defaultNow(),
});
