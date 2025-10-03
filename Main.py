import os, time
from instagrapi import Client
from instagrapi.exceptions import TwoFactorRequired, ChallengeRequired

# Config from env
USERNAME = os.getenv("ghost77928")
PASSWORD = os.getenv("raju79")
THREAD_ID = os.getenv("2044784296294178")          # required
NAMES_CSV = os.getenv("PRIXNE chuda", "prince ki maa randy ")      # comma separated names
SLEEP_SECS = int(os.getenv("SLEEP_SECS", "2"))  # default 2s

if not USERNAME or not PASSWORD or not THREAD_ID:
    print("ERROR: IG_USERNAME, IG_PASSWORD and GC_THREAD_ID must be set as environment variables.")
    raise SystemExit(1)

NAMES = [n.strip() for n in NAMES_CSV.split(",") if n.strip()]
if not NAMES:
    NAMES = ["prince ki maa randy","PRIXNE chuda" ]

def login():
    cl = Client()
    try:
        # try reuse settings if available on first run on server
        if os.path.exists("session_settings.json"):
            cl.load_settings("session_settings.json")
            cl.login(USERNAME, PASSWORD)
        else:
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings("session_settings.json")
        print("✅ Logged in as:", USERNAME)
        return cl
    except TwoFactorRequired:
        print("Two-factor required — complete 2FA manually and re-run.")
        raise
    except ChallengeRequired:
        print("Challenge required — solve on Instagram app and re-run.")
        raise
    except Exception as e:
        print("Login failed:", e)
        raise

def main():
    cl = login()
    i = 0
    while True:
        name = NAMES[i % len(NAMES)]
        try:
            # primary method
            try:
                cl.direct_thread_rename(THREAD_ID, name)
            except Exception:
                # fallback if method name differs
                cl.direct_thread_update_title(THREAD_ID, name)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✅ Changed TO: {name}")
            i += 1
        except Exception as e:
            print("Error while renaming:", repr(e))
        time.sleep(SLEEP_SECS)

if __name__ == "__main__":
    main()
