# AdoptCare VetBot (Discord, regex-only)

A simple rule-based chatbot that answers **pre-adoption pet health FAQs** using regex.  
⚠️ This bot provides general guidance only and is **not** a substitute for a veterinarian.

---

## Requirements
- Python **3.10+**
- Git
- A Discord bot **token** (from the [Discord Developer Portal](https://discord.com/developers/applications))
- Bot invited to your server with permissions:
  - **View Channels**
  - **Read Message History**
  - **Send Messages**

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/adoptcare-discord.git
cd adoptcare-discord
```

---

### 2. Create and activate a virtual environment

#### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Linux / macOS
```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Copy the template `.env.example` file and add your Discord bot token.

#### Windows
```powershell
Copy-Item .env.example .env
```

#### Linux / macOS
```bash
cp .env.example .env
```

Edit `.env` and paste your token:
```
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
```

---

### 5. (Optional) Run tests
```bash
pytest -q
```

---

### 6. Start the bot
```bash
python bot.py
```

If successful, you should see:
```
Logged in as AdoptCare VetBot#1234
```

---

### 7. Use the bot in Discord

In a channel where the bot has access, try:

```text
!help
```

Other examples:
- `I want to adopt a 3 month old kitten`
- `What vaccines does a kitten need?`
- `How often should I deworm a puppy?`
- `My dog has fleas`
- `When to spay a female cat?`
- `Feeding plan for a 3 month old kitten`
- `My dog has pale gums`

---

## Notes
- The bot must stay running in your terminal to stay online.
- Logs are saved in `logs/bot.log`.
