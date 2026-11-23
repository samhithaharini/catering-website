# Amutham React frontend

This React/Vite app is the website frontend. The Python API server is in the sibling `backend` folder and provides the quote API.

## Run locally

1. In a terminal, install backend dependencies and start the API:

   ```powershell
   cd C:\Users\Asus\Downloads\feast\backend
   py -m pip install -r requirements.txt
   py server.py
   ```

2. In a second terminal, start the React frontend:

   ```powershell
   cd C:\Users\Asus\Downloads\feast\frontend
   npm run dev
   ```

3. Open the Vite URL shown in the terminal (usually `http://localhost:5173`). The full menus page is at `/menus`.

The Vite development server proxies `/api` requests to the Python server at `http://127.0.0.1:8000`. Local enquiries use SQLite by default. Production can set `VITE_API_BASE_URL` to the deployed API origin; the backend uses PostgreSQL through `DATABASE_URL`.

Run `npm run build` to create the production frontend in `frontend/dist`. The Vercel project should use this directory as its root and set `VITE_API_BASE_URL` to the backend's Vercel URL.

