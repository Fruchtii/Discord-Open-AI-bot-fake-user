# discord-fake-user-bot

A Discord bot that blends into chat by responding like a real user. Supports **Google Gemini** (free tier) and **OpenAI** as AI providers.

> **Free tier note:** OpenAI no longer allows API access on their free tier. Use Gemini — it's free and works out of the box.

## Features

- Responds naturally to messages in any channel it has access to
- Maintains per-channel conversation history (last 10 messages)
- Supports Google Gemini (free) and OpenAI (paid)
- `!reset` command clears the bot's memory for the current channel
- Auto-deploys to your server on every push to `main` via GitHub Actions

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/Fruchtii/discord-fake-user-bot.git
cd discord-fake-user-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure

Edit `config.json`:

```json
{
  "discord_token": "YOUR_DISCORD_BOT_TOKEN",
  "provider": "gemini",
  "openai_api_key": "YOUR_OPENAI_API_KEY",
  "gemini_api_key": "YOUR_GEMINI_API_KEY"
}
```

Set `"provider"` to `"gemini"` or `"openai"`.

- **Gemini API key (free):** [aistudio.google.com](https://aistudio.google.com) → Get API key
- **OpenAI API key:** [platform.openai.com](https://platform.openai.com) → API keys (paid tier required)

### 4. Run

```bash
python bot.py
```

---

## Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2. Under the **Bot** tab, click **Add Bot** and copy the token into `config.json`.
3. Under **Privileged Gateway Intents**, enable **Message Content Intent**.
4. Under **OAuth2 → URL Generator**, select the `bot` scope and grant at minimum:
   - Read Messages / View Channels
   - Send Messages
   - Read Message History
5. Open the generated URL and add the bot to your server.

---

## Deployment

### Server Setup (first time)

These steps set the bot up as a systemd service so it restarts automatically.

```bash
# On your server
sudo apt update && sudo apt install python3-pip python3-venv git -y

git clone https://github.com/Fruchtii/discord-fake-user-bot.git
cd discord-fake-user-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Fill in your `config.json`, then create a systemd service:

```bash
sudo nano /etc/systemd/system/discord-fake-user-bot.service
```

```ini
[Unit]
Description=Discord Fake User Bot
After=network.target

[Service]
User=YOUR_LINUX_USER
WorkingDirectory=/home/YOUR_LINUX_USER/discord-fake-user-bot
ExecStart=/home/YOUR_LINUX_USER/discord-fake-user-bot/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-fake-user-bot
sudo systemctl start discord-fake-user-bot
```

### Auto-Deploy with GitHub Actions

Every push to `main` automatically deploys to your server. Add these secrets in your repo under **Settings → Secrets and variables → Actions**:

| Secret | Value |
|---|---|
| `SSH_HOST` | Your server's IP or hostname |
| `SSH_USER` | Linux user on the server |
| `SSH_PRIVATE_KEY` | Private SSH key with access to the server |
| `SSH_PORT` | SSH port (optional, defaults to 22) |
| `DEPLOY_PATH` | Absolute path to the bot directory on the server |

Once the secrets are set, push to `main` and the bot redeploys automatically.

---

## Contributing

Pull requests are welcome. For major changes, open an issue first.

## License

[MIT](LICENSE)
