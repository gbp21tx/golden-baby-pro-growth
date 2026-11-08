"""Deterministic, zero-cost daily content planner. No external calls or API keys."""
from datetime import datetime, timezone
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'campaign_output'
OUT.mkdir(exist_ok=True)
ARTIST = 'Golden Baby Pro'
URL = 'https://open.spotify.com/artist/65MKFTLOAXsO7LKw09sMPh'
SONGS = ['Shine Regardless', 'Live & Direct', 'Grindin’ Daily', 'All Around the World', 'Gametime', 'Much Throwder', 'Righteous King Vision', 'Back Against the Wall', 'Salute', 'Yung, Fly, and Flashy', 'Forever', 'Razzle Dazzle', 'Heaven 2 Me', 'I Like']
CHANNELS = ['Instagram Reels', 'TikTok', 'YouTube Shorts', 'Facebook']
ANGLES = [
 ('The story behind the track', 'Film a 15-second clip explaining what inspired this song.'),
 ('Performance moment', 'Film a clean 15-second performance excerpt using audio you have rights to.'),
 ('Question for listeners', 'Film a short introduction and ask what line resonates most.'),
 ('Studio process', 'Show a genuine behind-the-scenes moment from recording or writing.'),
 ('Introduce the artist', 'Record a short artist introduction and invite new listeners to explore the music.'),
 ('Lyrics spotlight', 'Display a short lyric excerpt you own and explain its meaning.'),
 ('Weekend discovery', 'Share a casual recommendation to check out this track and discuss it.')
]
now = datetime.now(timezone.utc)
day = now.date().isoformat()
idx = now.date().toordinal()
song = SONGS[idx % len(SONGS)]
angle, concept = ANGLES[idx % len(ANGLES)]
platform = CHANNELS[idx % len(CHANNELS)]
caption = f'{angle}: “{song}” by {ARTIST}. What stands out to you? Listen to the music on Spotify: {URL} #GoldenBabyPro #IndependentHipHop #NewMusicDiscovery'
content = f'''# Golden Baby Pro — Daily Campaign Brief ({day} UTC)\n\n**Featured song:** {song}\n\n**Suggested channel:** {platform}\n\n**Creative angle:** {angle}\n\n**15-second video concept:** {concept}\n\n## Draft caption (review before publishing)\n\n{caption}\n\n## Today's manual checklist\n\n- [ ] Record or select a rights-cleared clip\n- [ ] Review and publish the caption on {platform}\n- [ ] Reply thoughtfully to genuine comments\n- [ ] Research one relevant independent playlist that accepts submissions\n- [ ] If there is a fit, draft a personalized, permission-based pitch\n- [ ] Log actual clicks and Spotify for Artists results when available\n\n**Note:** This is a zero-cost scheduled content planner, not a generative model. It does not auto-post, message anyone, or create streams.\n'''
(OUT / 'latest_campaign.md').write_text(content, encoding='utf-8')
with (OUT / 'campaign_history.csv').open('a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(['date_utc', 'song', 'platform', 'angle', 'spotify_url'])
    writer.writerow([day, song, platform, angle, URL])
print(content)
