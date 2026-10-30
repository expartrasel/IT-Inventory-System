# Two Star Technology

A responsive Bengali storefront for an IT product and repair business in Dhaka. Includes laptop, desktop, printer, CCTV, SSD, HDD, RAM, processor, memory card, monitor and USB drive categories; search, sorting, product details, server-persisted guest carts, delivery pricing, cash-on-delivery requests, repair bookings and private order tracking using an order reference and phone number.

The catalogue contains illustrative products and sample prices, explicitly marked on the website. Edit `public/catalog.js` to publish confirmed models, prices, warranty terms and availability. Product illustrations are original SVGs. Service starts at BDT 300; parts and final repairs are quoted separately.

## Hosting and database

Netlify serves `public/` and the API in `netlify/functions/store.mts`. Netlify Database stores carts, orders and service bookings using Drizzle. The schema is in `db/schema.ts`; the generated migration is under `netlify/database/migrations/`. The platform applies migrations during deployment. Do not run migrations manually. Legacy Django files are outside the published directory and are not used by this storefront.

Use `netlify dev --port 8889` for local preview. Database-backed end-to-end testing requires a database on which the platform has applied the migration.

## Payments

The SSLCommerz hosted-checkout adapter is implemented for wallet payments, including bKash, Nagad and Rocket when enabled on the merchant account. Configure the merchant account securely through Netlify runtime environment settings using `SSLCOMMERZ_STORE_ID`, `SSLCOMMERZ_STORE_PASSWORD` and `SSLCOMMERZ_MODE`. Set the mode to `live` only after merchant approval and successful sandbox testing. Never put credentials in source code or chat.

The shop owner confirmed that no merchant account is currently available. Cash on delivery is the active payment method; online checkout remains disabled until an approved merchant account is configured. Sandbox mode is clearly labelled. The app never requests wallet PINs or OTPs. Callbacks and IPNs are validated directly with the gateway, with transaction ID, currency and order total checked before recording payment. Risky payments are held for review. Callback query strings are presentation only; phone-verified tracking retrieves the actual stored payment status.

Merchant account activation and a real sandbox/live gateway transaction have not been completed. Accepted wallet channels depend on the merchant agreement. A pending online order remains trackable when checkout is interrupted; a retry or refund requires merchant follow-up.

## Business information before launch

Add the shop's real contact number, detailed address, confirmed delivery/return policy and real inventory. Delivery prices of BDT 80 in Dhaka and BDT 150 outside Dhaka are initial defaults and should be confirmed. Requests are saved for business follow-up; this change does not include an order-management dashboard, automated notifications, stock management or automated refunds.

## Verification

- `npm test`: server-side price, quantity and Bangladeshi phone validation.
- `npm run check`: TypeScript verification.
- `npx playwright test tests/storefront.spec.mjs tests/api.spec.mjs`: UI flow tests use simulated database API responses, while API validation tests call the local function directly. Start Netlify Dev first.
