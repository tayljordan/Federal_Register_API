import requests
import os

def download_latest_ecfr(title: int, out_dir: str):
    """
    Download the latest eCFR XML for a given CFR title.
    """
    os.makedirs(out_dir, exist_ok=True)

    url = f"https://www.govinfo.gov/bulkdata/ECFR/title-{title}/ECFR-title{title}.xml"
    out_path = os.path.join(out_dir, f"ECFR-title{title}.xml")

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    with open(out_path, "wb") as f:
        f.write(r.content)

    print(f"✅ Downloaded latest eCFR Title {title}")
    print(f"📄 Saved to: {out_path}")


if __name__ == "__main__":
    # Example: download Title 46 (Shipping)
    download_latest_ecfr(
        title=46,
        out_dir="ecfr/downloads"
    )
