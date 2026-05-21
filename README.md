# MedCore Website

A starter static website for the MedCore project, implementing an introductory product landing page with background, product features, architecture, research insights, and team messaging.

## Files

- `index.html` — main landing page
- `styles.css` — responsive styling
- `script.js` — mobile navigation toggle

## Local preview

Open `MedCore-Website/index.html` in your browser to preview the site.

If you have a local static server installed, you can also serve the folder from the workspace root:

```bash
cd "c:\Users\ikeme\Documents\DTC Hackathon\MedCore-Website"
python -m http.server 8000
```

Then open `http://localhost:8000`.

## GitHub Pages deployment

This static website is deployed with the workflow in `.github/workflows/deploy-pages.yml`.

- In the GitHub repository, open **Settings > Pages**.
- Set **Build and deployment > Source** to **GitHub Actions**.
- Push to `main` or `master`, or run the workflow manually from the **Actions** tab.
- Keep all links relative so the site works from a GitHub Pages path.
- When you later register a custom domain, add a `CNAME` file in the repository root containing your domain name.

## Contact

Use `getmedcore@gmail.com` for all outreach and inquiries about the MedCore project.
