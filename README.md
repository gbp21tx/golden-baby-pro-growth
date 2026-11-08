# Golden Baby Pro — AI Spotify Growth Bot

A local Streamlit marketing dashboard for legitimate Spotify audience growth. It drafts AI social content (with your OpenAI API key), builds playlist outreach messages, and tracks campaign metrics in a local SQLite database.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL displayed in your terminal. Add the artist's official Spotify URL in the sidebar. Optionally supply your OpenAI API key to generate posts. API usage may incur costs.

## Safety

No automated Spotify plays, scraping, unsolicited bulk messaging, fake accounts, fake engagement, or guaranteed playlist placement. Metrics are manually entered, not live Spotify API data. Goals are aspirational, not forecasts.

Official artist profile configured: https://open.spotify.com/artist/65MKFTLOAXsO7LKw09sMPh

## Free scheduled cloud automation (GitHub Actions)

1. Create a **private** GitHub repository and upload the **contents** of this folder to the repository root (the `.github` folder must be included). Do not upload API keys or personal data.
2. In the repository, open **Actions**, enable workflows if prompted, and select **Golden Baby Pro Daily Campaign** > **Run workflow** to test it.
3. Open the completed run and download the `golden-baby-pro-daily-brief` artifact. It contains a Markdown campaign brief and a CSV log for that run.
4. The workflow is scheduled daily at **15:00 UTC** (9 AM CST / 10 AM CDT). GitHub may delay or disable scheduled runs for inactive repositories; check Actions regularly.
5. Review each brief, record a rights-cleared short video, and publish manually. This setup does not connect to or automatically post on social networks.
6. Check Spotify for Artists weekly and enter actual results into the local dashboard, or keep a separate tracking sheet. The GitHub artifact is not a persistent database; each run contains its own CSV.

**Important:** The scheduled workflow uses a free, deterministic rotating content template (not paid generative AI). The Streamlit dashboard's optional OpenAI generation requires an API key and may incur charges. GitHub free-tier quotas and policies can change. GitHub Actions is a scheduler, not a permanently running 24/7 server; the Streamlit dashboard remains local unless separately hosted. No Spotify streams, engagement, playlist placements, or auto-posts are generated.
