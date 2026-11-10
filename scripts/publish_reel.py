import csv, datetime, json, os, sys, time
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from zoneinfo import ZoneInfo

scheduled = os.getenv("EVENT_NAME") == "schedule"
dry_run = (os.getenv("DRY_RUN") or "true").lower() == "true" if not scheduled else False
if scheduled and os.getenv("ENABLE_AUTO_REELS") != "true":
    print("Scheduled posting disabled. Set repository variable ENABLE_AUTO_REELS=true after review.")
    sys.exit(0)

with open("reels/schedule.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))
today = datetime.datetime.now(ZoneInfo("America/Chicago")).strftime("%A")
entry = next(row for row in rows if row["day"] == today)
base_url = os.getenv("REELS_PUBLIC_BASE_URL", "").strip().rstrip("/")
if not base_url:
    raise RuntimeError("Missing repository variable REELS_PUBLIC_BASE_URL")
# Alternate the original and approved likeness artwork every calendar week.
# A missing V2 asset must never break the existing daily publisher.
original_file = entry["file"]
v2_file = original_file.replace(".mp4", "_v2.mp4")
use_v2 = datetime.datetime.now(ZoneInfo("America/Chicago")).isocalendar().week % 2 == 0
selected_file = v2_file if use_v2 else original_file
video_url = base_url + "/" + quote(selected_file)
if not video_url.startswith("https://"):
    raise RuntimeError("Public media URL must use HTTPS")
if use_v2:
    try:
        with urlopen(Request(video_url, method="HEAD"), timeout=20) as response:
            if response.status != 200 or "video/" not in response.headers.get("Content-Type", ""):
                raise ValueError("New video is not available as a video resource")
    except Exception as error:
        print("New artwork video unavailable; using original:", type(error).__name__)
        selected_file = original_file
        video_url = base_url + "/" + quote(original_file)
print("Day:", today, "Song:", entry["song"])
print("Rotation:", "new likeness" if selected_file == v2_file else "original")
print("Video URL:", video_url)
if dry_run:
    print("DRY RUN; no post sent. Caption:", entry["caption"])
    sys.exit(0)
token = os.getenv("META_ACCESS_TOKEN", "").strip()
user_id = os.getenv("INSTAGRAM_USER_ID", "").strip()
if not token or not user_id:
    raise RuntimeError("Missing GitHub secrets META_ACCESS_TOKEN or INSTAGRAM_USER_ID")
api = "https://graph.facebook.com/v27.0"
def request(endpoint, params, method="GET"):
    params = {**params, "access_token": token}
    url = f"{api}/{endpoint}"
    data = urlencode(params).encode() if method == "POST" else None
    if method == "GET":
        url += "?" + urlencode(params)
    try:
        with urlopen(Request(url, data=data, method=method), timeout=60) as response:
            return json.load(response)
    except HTTPError as error:
        try:
            details = json.loads(error.read().decode("utf-8", "replace")).get("error", {})
            print("Meta API error:", json.dumps({k: details.get(k) for k in ("message", "code", "error_subcode", "type")}))
        except ValueError:
            print("Meta HTTP error", error.code)
        raise RuntimeError(f"Meta API HTTP {error.code}") from None

print("Creating Instagram Reel container")
container = request(f"{user_id}/media", {
    "media_type": "REELS",
    "video_url": video_url,
    "caption": entry["caption"],
    "share_to_feed": "true"
}, method="POST")["id"]
for attempt in range(36):
    info = request(container, {"fields": "status_code,status"})
    status = info.get("status_code")
    print("Processing:", status)
    if status == "FINISHED":
        break
    if status in ("ERROR", "EXPIRED"):
        raise RuntimeError("Meta processing failed: " + str(info.get("status", status)))
    time.sleep(10)
else:
    raise TimeoutError("Reel processing timed out")
published = request(f"{user_id}/media_publish", {"creation_id": container}, method="POST")
print("Published Reel ID:", published["id"])
