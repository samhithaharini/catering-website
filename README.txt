Amutham website

The website frontend is a React application built with Vite and Bootstrap 5.
The backend is a FastAPI service. It uses SQLite for local development and
PostgreSQL when DATABASE_URL is configured. Quote requests are validated and
saved before optional staff email notifications are sent.

RUN LOCALLY
  1. Install Node.js and Python 3.
  2. Install the API dependencies:
       cd C:\Users\Asus\Downloads\feast\backend
       py -m pip install -r requirements.txt
  3. In a terminal, start the quote API from the backend folder:
       cd C:\Users\Asus\Downloads\feast\backend
       py server.py
  4. In a second terminal, start the React app:
       cd C:\Users\Asus\Downloads\feast\frontend
       npm run dev
  5. Open the Vite URL shown in the second terminal (usually http://localhost:5173).
  6. Stop each process with Ctrl+C in its terminal.

The React app proxies /api requests to the Python server at 127.0.0.1:8000.
Without DATABASE_URL, local enquiries are stored in backend\data\quotes.db.
The Python server provides the quote API only; it does not host the React frontend.
Backend modules and their responsibilities are documented in backend\README.md.

Customers submit enquiries without creating an account. Enquiries are saved in
the configured database, and notifications are queued and sent by email when
FEAST_SMTP_HOST, FEAST_NOTIFICATION_FROM, and FEAST_NOTIFICATION_TO are
configured. Failed deliveries are retried so the business can contact the customer.

LOCAL EMAIL NOTIFICATIONS
  1. Open .env in the project folder. Gmail's server and port are already set.
  2. Set FEAST_SMTP_USER to the Gmail address that will send notifications.
     Set FEAST_NOTIFICATION_FROM to that same address, and
     FEAST_NOTIFICATION_TO to the inbox where the business should receive them.
  3. Create a Google App Password and put it in FEAST_SMTP_PASSWORD. App
     Passwords require 2-Step Verification. Do not use your regular Gmail
     password. See https://support.google.com/accounts/answer/185833.
  4. Restart the backend. New enquiries will be emailed to
     FEAST_NOTIFICATION_TO. If SMTP is not configured, enquiries are still
     saved in the configured database, but no email alert is sent.

For local SQLite data, create a consistent backup with `py server.py --backup`.
The SQLite migration script copies local enquiries to PostgreSQL. For deployed
PostgreSQL data, use the database provider's backup and retention tools.

## Deploy the website on Vercel

Vercel's function filesystem is temporary, so production enquiries must use
PostgreSQL. This project deploys the frontend and FastAPI API as separate
Vercel projects and connects the API to a PostgreSQL database provider.

  1. Push this project to a GitHub repository. Do not commit .env.
  2. Create a PostgreSQL database with your chosen provider and copy its
     connection URL.
  3. Import this repository in Vercel for the API project. Set Root Directory
     to backend and add DATABASE_URL (pooled), DATABASE_URL_UNPOOLED (direct
     migrations), CRON_SECRET, plus the Gmail SMTP variables if email alerts
     are wanted. Deploy and copy the API project's URL.
  4. Import the repository again in Vercel for the website. Set Root Directory
     to frontend and set VITE_API_BASE_URL to the API project's URL. Deploy.
  5. In the API project's Vercel settings, set FEAST_CORS_ORIGINS to the exact
     website URL, including https://, and redeploy the API.
  6. Submit a test enquiry and confirm it is saved and the email arrives. The
     API health address is the API URL plus /health.

The Vercel configuration keeps client-side routes such as /menus working.
Local development uses SQLite and the Vite proxy by default. To move existing
local enquiries into PostgreSQL, set DATABASE_URL in .env and run
`py migrate_sqlite_to_postgres.py` from the backend folder.

## Deploy with Docker Compose

Copy `.env.example` to `.env`, set DOMAIN to a DNS name pointing at the host,
and configure SMTP if enquiry notifications are needed. Then run
`docker compose up --build -d`. Caddy serves the built frontend,
proxies API requests to the private API container, and obtains TLS certificates
for DOMAIN. Allow inbound ports 80 and 443 on the host firewall. When
DATABASE_URL is blank, SQLite data is kept in the persistent `feast-data`
Docker volume. Keep `.env` and
database backups private, encrypt off-host backup copies, and protect the Docker
host with disk encryption and restricted access. API logs include request paths
and client IP addresses but never quote field contents; apply a log retention
policy too. Configure and periodically test a backup copy stored outside the
host; the named volume alone is not a backup. Select a quote retention period
for your business before using the purge command.

See frontend\README.md for more information. Do not expose the development
server directly to the internet.
