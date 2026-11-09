# Golden Baby Pro — Daily Instagram Reels (review branch)

This is a staging-only setup. Existing `.github/workflows/instagram-publish.yml` is unchanged.

1. Review the seven MP4 files in the starter ZIP supplied in ChatGPT. Verify all audio, samples, likenesses, and artwork rights.
2. Upload the seven videos to `reels/` in this repository. GitHub Pages must be enabled from `main` / root only *after* files are on main. This branch intentionally contains no video files yet.
3. Configure `Settings > Pages > Deploy from a branch` (`main`, root). Once enabled and videos merged, verify direct MP4 link in a private window: `https://gbp21tx.github.io/golden-baby-pro-growth/reels/monday_grindin_daily.mp4`.
4. In `Settings > Secrets and variables > Actions > Variables`, set `REELS_PUBLIC_BASE_URL` to `https://gbp21tx.github.io/golden-baby-pro-growth/reels` and `ENABLE_AUTO_REELS` to `false`. The URL is an example until Pages is tested.
5. Confirm the existing `META_ACCESS_TOKEN` and `INSTAGRAM_USER_ID` repository secrets (do not share values). Rotate any access token previously shown in a screenshot.
6. Merge the reviewed branch after the media is hosted. Go to Actions > Golden Baby Pro Daily Instagram Reels > Run workflow and choose `dry_run=true`. Review logs and video URL.
7. After verifying availability, permissions, and a *single* manual `dry_run=false` Reel published successfully, change `ENABLE_AUTO_REELS` to `true`.
8. Scheduled GitHub workflows can be delayed or dropped; target time is 15:00 UTC daily (9 AM CST or 10 AM CDT). The local weekday determines the song.

Meta Reel publishing needs public direct MP4 URLs; local GitHub action files alone are insufficient for remote fetch. Existing image posting remains independent. Publishing is *not* activated by creating or merging this branch alone.
