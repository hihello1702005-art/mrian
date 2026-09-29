# Meradio'N — Your Sound. Your Stories.

Meradio'N is a premium live-radio platform with a Flutter listener/RJ app, FastAPI orchestration layer, and React operations dashboard. Its live path is **Flutter → FastAPI → AzuraCast → listeners**; remote two-RJ sessions use **LiveKit → AzuraCast**, while recordings move from live capture through processing/storage to the archive.

## Included
- Material 3 Flutter application with warm olive, beige, rust and chocolate editorial design; splash, home, live player, schedule, archive, profile/favorites/notification entry points, mini-player, and RJ studio.
- FastAPI REST API with JWT login/register, role checks (USER/RJ/ADMIN), validation, CORS, radio/status endpoints, show/schedule/recording/favorite/notification/analytics routes, AzuraCast proxy and server-only LiveKit token minting.
- PostgreSQL/Supabase-compatible schema with relational constraints and indexes.
- Vite React/TypeScript admin dashboard with responsive operations layout and listener trend chart.
- Demo Mode that keeps the product usable without AzuraCast, LiveKit, Firebase, Supabase, or storage credentials.

## Quick start
```bash
cp backend/.env.example backend/.env
cd backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
uvicorn app.main:app --reload
# another terminal
cd admin && cp .env.example .env && npm install && npm run dev
# another terminal (Flutter SDK required)
cd mobile && cp .env.example .env && flutter pub get && flutter run
```
Run `docker compose up --build` for PostgreSQL and the backend. Apply `database/schema.sql` to Supabase/PostgreSQL; production authentication may federate Supabase Auth, while this service provides JWT authorization for its APIs.

## Demo accounts
`admin@meradion.app` / `Admin123!` (ADMIN) and `sai@meradion.app` / `Radio123!` (RJ). Use only in Demo Mode.

## Configuration and integrations
All secrets stay in environment files: never expose AzuraCast API keys, LiveKit secrets, Supabase service role credentials, storage keys, or Firebase private keys. Configure AzuraCast (`AZURACAST_*`) for station metadata and streams, LiveKit (`LIVEKIT_*`) for signed temporary RJ room tokens, Supabase credentials/storage for production records, and Firebase platform files for production push delivery. The Flutter app only receives an API URL and a short-lived LiveKit token.

## Verification
```bash
cd backend && pytest
cd admin && npm run build
cd mobile && flutter analyze && flutter test
```
External radio, room publishing, storage uploads and FCM delivery require their respective deployed credentials and platform configuration. See [docs](docs/SETUP.md) for operational setup, deployment and troubleshooting.
