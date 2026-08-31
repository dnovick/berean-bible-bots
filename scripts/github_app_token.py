"""Generate a GitHub App installation token for berean-bots-author or berean-bots-reviewer.

Local config (~/.config/berean-bots/github-apps.json):
{
  "author": {
    "app_id": 123456,
    "installation_id": 78901234,
    "private_key_path": "~/.config/berean-bots/author-01-app.pem"
  },
  "reviewer": {
    "app_id": 123457,
    "installation_id": 78901235,
    "private_key_path": "~/.config/berean-bots/reviewer-01-app.pem"
  }
}

CI mode (environment variables override the config file):
  ROLE_APP_ID, ROLE_PRIVATE_KEY, ROLE_INSTALLATION_ID
  where ROLE is AUTHOR or REVIEWER (uppercased --role value).

Usage:
  GH_TOKEN=$(python scripts/github_app_token.py --role author)
  GH_TOKEN=$(python scripts/github_app_token.py --role reviewer)
"""

import argparse
import json
import os
import time
from pathlib import Path

import jwt
import requests


CONFIG_PATH = Path.home() / ".config" / "berean-bots" / "github-apps.json"


def get_installation_token(app_id: int, private_key: str, installation_id: int) -> str:
    now = int(time.time())
    payload = {
        "iat": now - 60,   # 60 s leeway for clock skew
        "exp": now + 600,  # 10-minute expiry (GitHub max for JWTs)
        "iss": str(app_id),
    }
    encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")

    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers={
            "Authorization": f"Bearer {encoded_jwt}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    response.raise_for_status()
    return str(response.json()["token"])


def load_credentials(role: str) -> tuple[int, str, int]:
    """Return (app_id, private_key, installation_id) for the given role.

    CI mode: reads from ROLE_APP_ID, ROLE_PRIVATE_KEY, ROLE_INSTALLATION_ID env vars.
    Local mode: reads from ~/.config/berean-bots/github-apps.json + .pem file.
    """
    prefix = role.upper()
    env_app_id = os.environ.get(f"{prefix}_APP_ID")
    env_key = os.environ.get(f"{prefix}_PRIVATE_KEY")
    env_install = os.environ.get(f"{prefix}_INSTALLATION_ID")

    if env_app_id and env_key and env_install:
        # GitHub Actions may encode newlines as literal \n in env vars
        env_key = env_key.replace("\\n", "\n")
        return int(env_app_id), env_key, int(env_install)

    if not CONFIG_PATH.exists():
        raise SystemExit(
            f"Config file not found: {CONFIG_PATH}\n"
            "Create it with app_id, installation_id, and private_key_path, "
            f"or set {prefix}_APP_ID / {prefix}_PRIVATE_KEY / {prefix}_INSTALLATION_ID env vars."
        )

    config = json.loads(CONFIG_PATH.read_text())[role]
    private_key_path = Path(config["private_key_path"]).expanduser()

    if not private_key_path.exists():
        raise SystemExit(f"Private key not found: {private_key_path}")

    return int(config["app_id"]), private_key_path.read_text(), int(config["installation_id"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a GitHub App installation token.")
    parser.add_argument("--role", choices=["author", "reviewer"], required=True,
                        help="Which app to generate a token for.")
    args = parser.parse_args()

    app_id, private_key, installation_id = load_credentials(args.role)
    token = get_installation_token(app_id, private_key, installation_id)
    print(token, end="")  # no trailing newline — safe for GH_TOKEN=$(...)


if __name__ == "__main__":
    main()
