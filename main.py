import yfinance as yf
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime

TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_URL = f"https://{TOKEN}@github.com/Drtatom/spy-tracker.git"
REPO_DIR = os.path.join(tempfile.gettempdir(), "spy-tracker-git")
REPORT_FILE = "spy_report.json"

def get_spy_data():
    ticker = "SPY"
    data = yf.Ticker(ticker)
    hist = data.history(period="1mo")

    current_price = hist['Close'].iloc[-1]
    moving_avg = hist['Close'].mean()

    report = {
        "ticker": ticker,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "price": round(float(current_price), 2),
        "moving_avg_30d": round(float(moving_avg), 2),
        "status": "bullish" if current_price > moving_avg else "bearish"
    }
    return report

def run_git(cmd, cwd=None):
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0 and "nothing to commit" not in result.stderr:
        print(f"Git error ({' '.join(cmd)}): {result.stderr.strip()}", file=sys.stderr)
        return False
    return True

if __name__ == "__main__":
    if not TOKEN:
        print("GITHUB_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    # Clone or pull
    if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
        run_git(["git", "clone", REPO_URL, REPO_DIR])
    else:
        run_git(["git", "-C", REPO_DIR, "pull", REPO_URL, "main"])

    # Generate report
    report = get_spy_data()
    report_path = os.path.join(REPO_DIR, REPORT_FILE)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    # Commit and push
    run_git(["git", "-C", REPO_DIR, "add", REPORT_FILE])
    if run_git(["git", "-C", REPO_DIR, "commit", "-m", f"chore: SPY report {datetime.now().strftime('%Y-%m-%d')}"]):
        run_git(["git", "-C", REPO_DIR, "push", REPO_URL, "main"])
