#!/usr/bin/env python3
"""Free, offline social-content queue. No platform logins or API calls."""
import csv
import datetime as dt
import hashlib
import os
from pathlib import Path

ARTIST = 'Golden Baby Pro'
SPOTIFY = 'https://open.spotify.com/artist/65MKFTLOAXsO7LKw09sMPh'
SONGS = ['Shine Regardless', 'Live & Direct', 'Grindin’ Daily', 'Back Against the Wall', 'Salute', 'Forever', 'Gametime']
PLATFORMS = ['Instagram Reels', 'TikTok', 'YouTube Shorts', 'Facebook Reels']
HOOKS = [
    'For anyone staying focused when the odds are against them',
    'A soundtrack for the days you refuse to quit',
    'Turn this up when you need to reset your mindset',
    'New music discovery for your next playlist',
    'Which line or moment stands out to you?',
    'Share this with someone chasing a goal',
    'Looking for independent hip-hop to add to your rotation?'
]
IDEAS = [
    '15-second performance clip with on-screen song title and artist name',
    'Behind-the-scenes studio clip with an opening text hook',
    'Lyric-style text animation using only artist-owned audio and artwork',
    'Artist talking to camera about the song’s inspiration',
    'Vertical cover-art reveal with a short licensed music excerpt',
    'Question prompt over a performance clip; invite genuine comments',
    'Short introduction to the artist and why the track matters'
]
HASHTAGS = '#GoldenBabyPro #IndependentHipHop #NewMusicDiscovery'

def generate(day):
    seed = int(hashlib.sha256(day.isoformat().encode()).hexdigest()[:8], 16)
    rows = []
    for offset in range(7):
        date = day + dt.timedelta(days=offset)
        idx = (seed + offset) % len(SONGS)
        song = SONGS[idx]
        for platform in PLATFORMS:
            caption = (f'{HOOKS[idx]}. 🎧 {ARTIST} — {song}. '
                       f'Listen on Spotify: {SPOTIFY} {HASHTAGS}')
            if platform == 'YouTube Shorts':
                caption = f'{ARTIST} — {song} | {HOOKS[idx]}. Listen: {SPOTIFY} #Shorts #GoldenBabyPro'
            rows.append({
                'date': date.isoformat(), 'platform': platform, 'song': song,
                'video_concept': IDEAS[idx], 'caption': caption,
                'spotify_url': SPOTIFY, 'status': 'DRAFT - REVIEW BEFORE POSTING'
            })
    return rows

def main():
    day = dt.date.fromisoformat(os.environ['CAMPAIGN_DATE']) if os.environ.get('CAMPAIGN_DATE') else dt.datetime.now(dt.timezone.utc).date()
    out = Path('social_output')
    out.mkdir(parents=True, exist_ok=True)
    rows = generate(day)
    with (out / 'seven_day_content_queue.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    lines = [f'# {ARTIST} — 7-Day Social Media Campaign', '', f'Generated: {day.isoformat()} (UTC)', '',
             f'Official Spotify artist page: {SPOTIFY}', '',
             '**Drafts only:** Review accuracy, permissions, links, and platform rules before publishing.',
             'Use only audio, visuals, and artwork you own or have permission to use.',
             'No auto-posting, auto-messaging, fake engagement, or artificial streams.', '',
             '## Daily publishing checklist', '',
             '- Choose one strong vertical video; adapt it for each platform.',
             '- Add a clear Spotify call to action where links are supported.',
             '- Reply to genuine comments personally; do not spam.',
             '- Record actual results weekly in Spotify for Artists and platform analytics.', '',
             '## Seven-day ideas', '']
    for i in range(7):
        r = rows[i * len(PLATFORMS)]
        lines += [f"### {r['date']} — {r['song']}", '', f"Video: {r['video_concept']}", '',
                  f"Sample Instagram/TikTok caption: {r['caption']}", '']
    (out / 'social_campaign_brief.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'Created {len(rows)} platform drafts in {out}/')

if __name__ == '__main__':
    main()
