# Redible Bot – Random Reddit Image Poster

Automates image posts to Reddit at **random times within a daily window**. You provide:

* `subreddits.txt` — list of target subreddits
* `titles.txt` — pool of post titles
* `images/` — folder of images

The bot picks a **random title + image + subreddit** for each scheduled time and posts via the Reddit API.
---

## ✨ Features

* ⏱️ **Daily scheduling**: choose a start & end hour; the bot randomly schedules N posts within that window.
* 🔀 **No-repeat subreddits per day**: avoids using the same subreddit twice until all are used.
* 🖼️ **Image submissions**: posts `jpg/png/jpeg/gif/heic` via `submit_image`.
* 🧪 **Interactive CLI**: prompts you for hours and how many posts to schedule (with safe caps).
* 🎛️ **Nice console UI**: figlet banner + color output.
* 🔐 **License check**: validates a license key against a server before running.

---

## 🧰 Requirements

* Python **3.9+**
* Packages 

  * `praw`, `requests`, `schedule`, `pyfiglet`, `colorama`

## 🔑 Credentials

The script loads Reddit credentials from a plain text file:

**`reddit_credentials.txt`**

```ini
client_id=YOUR_CLIENT_ID
client_secret=YOUR_CLIENT_SECRET
username=YOUR_REDDIT_USERNAME
password=YOUR_REDDIT_PASSWORD
```

> Create a Reddit **script app** at [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) to obtain `client_id` and `client_secret`.

**Security tips**

* Add `reddit_credentials.txt` to `.gitignore`.
* Consider switching to environment variables or a `.env` file in the future.
* If credentials were ever committed, rotate them.

---

## 📥 Input files & structure

```
Reddit_bot/
├─ main.py (or your script file)
├─ reddit_credentials.txt               # NOT committed
├─ subreddits.txt                       # one subreddit per line (no `r/`)
├─ titles.txt                           # one title per line
└─ images/                              # image files (jpg/png/jpeg/gif/heic)
```

**`subreddits.txt` example**

```
memes
funny
cats
```

**`titles.txt` example**

```
This made my day
POV: Monday hits back
Couldn’t stop laughing at this
```

---

## 🚀 Run

Start the bot from the project folder:

```bash
python main.py
```

You will be prompted for:

1. **License key** (validated via the configured license server)
2. **Start hour (0–23)**
3. **End hour (0–23)**
4. **Posts per day** (must be < 10)

The bot then prints each scheduled time (e.g., `scheduled post at 14:27`) and stays running, posting at the scheduled moments. Press **CTRL‑C** to exit.

---

## 🧠 How it works

* Shows a banner (`pyfiglet` + `colorama`).
* Validates a license key by POSTing to the server.
* Reads credentials from `reddit_credentials.txt` and connects to Reddit via `praw.Reddit`.
* Scans `images/` and filters supported extensions.
* Reads `titles.txt` and `subreddits.txt`.
* Schedules `N` random `HH:MM` times between your start/end hours using `schedule`.
* On each run, picks a random (title, image, subreddit). **Each subreddit is used at most once per day.**
* Submits using `subreddit.submit_image(title=..., image_path=...)`.

---

## 🛡️ Good citizen checklist

* Respect each sub’s rules (flairs, OC, repost policies).
* Keep posting frequency reasonable (the app caps daily posts < 10 to avoid spam).
* Use unique, relevant titles.
* Handle mod messages and removals.

---

## 🧯 Troubleshooting

* **License invalid**: Double‑check the key; ensure outbound HTTPS allowed.
* **Reddit auth fails**: Verify credentials, rotate password if needed.
* **`you are doing that too much`**: You hit rate limits—reduce daily posts or widen the time window.
* **Image won’t post**: Confirm the file exists and is a supported type; paths are relative to the script folder.
* **No posts happen**: Ensure the process remains running; check your system clock/timezone.

---

## 🔒 Prevent committing secrets

Add a `.gitignore` entry:

```gitignore
reddit_credentials.txt
```

If secrets were ever pushed, rewrite history (e.g., with `git filter-repo` or BFG) and **rotate** them.

---

## 🪪 License

MIT

---

## 🙌 Credits

Built with ❤️ using `praw`, `requests`, `schedule`, `pyfiglet`, and `colorama`.

