# Planvesto Next.js migration

Migrated from the supplied multi-page static HTML files.

The page markup and Tailwind visual system are preserved. Internal `.html` links are converted to Next.js routes. Existing mobile navigation and Learn-page search behavior are handled in React.

Authentication remains frontend-only, matching the supplied HTML. No backend/authentication system has been added.

Commands:
npm install
npm run dev
npm run build
npm start
