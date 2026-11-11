# Approved Golden Baby Pro Reels: 14-video rotation

The seven new **15-second** MP4s were approved in ChatGPT. They are not included in this pull request; GitHub Actions **cannot** publish them until they are added to the repository and accessible through GitHub Pages.

## Upload to `reels/`
- monday_grindin_daily_v2.mp4
- tuesday_yung_fly_and_flashy_v2.mp4
- wednesday_all_around_the_world_v2.mp4
- thursday_gametime_v2.mp4
- friday_razzle_dazzle_v2.mp4
- saturday_forever_v2.mp4
- sunday_righteous_king_vision_v2.mp4

Get files from `golden_baby_pro_7_new_likeness_reels.zip` provided in your ChatGPT conversation. Upload MP4s to `reels/` on this review branch. Keep the existing seven MP4s unchanged.

## Behavior
This PR adds alternating calendar-week selection (ISO week parity). The existing daily song schedule, Meta token secrets, and GitHub Actions workflow remain unchanged.

On an alternating week, the publisher will try the new `_v2.mp4` for today's song. If the URL does not respond with a direct HTTP 200 video resource, it falls back to the original, rather than break the daily scheduled publication. A dry run will show which video was selected.

## Safe rollout
1. Upload all seven new videos to this branch, and review their rights and media quality.
2. Merge PR after review. Allow GitHub Pages to deploy; verify all seven `_v2.mp4` direct public URLs.
3. Run `Golden Baby Pro Daily Instagram Reels` with `dry_run=true` to verify the selection.
4. Keep `ENABLE_AUTO_REELS=false` while manually testing `dry_run=false` (if you want to publish another Reel), avoiding duplicates.
5. Re-enable `ENABLE_AUTO_REELS=true` only after confirming new videos are reachable and at least one new variation publishes.

Note: scheduled runs follow UTC cron 15:00 and select weekday in America/Chicago; GitHub scheduling can be delayed. This PR does not add automatic Meta token renewal or duplicate prevention.
