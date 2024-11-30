# Andronel - AI-Powered Discord Bot

Andronel is a lightweight Discord bot that integrates Google Generative AI's **Gemini API** for intelligent chat responses. It also includes voice channel management commands, making it a helpful addition to any Discord server.

---

## Features

1. **AI Chat Integration**  
   - Use the `!ask` command to get answers or generate content using Gemini AI.
   - Automatically splits responses exceeding Discord's 2000-character limit.

2. **Voice Channel Management**  
   - `!androjoin`: Bot joins your current voice channel.  
   - `!androleave`: Bot leaves the voice channel.

3. **Basic Chat Commands**  
   - `!hello`: Greets the user.

---

## Setup

### Requirements
- Python 3.8+  
- **Discord Bot Token** (from [Discord Developer Portal](https://github.com/indronero/Andronel-Bot.git)).  
- **Google Gemini API Key** (get access [here](https://developers.generativeai.google/)).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/andronel.git
   cd andronel

2. Install dependencies:
   pip install discord.py google-generativeai

3. Create an apikeys.py file:
   botToken = "YOUR_DISCORD_BOT_TOKEN"
   geminiToken = "YOUR_GEMINI_API_KEY"

4. Run the bot:
   python3 main.py

### Commands
!hello - Sends a friendly greeting.
!ask [question]	- Queries the AI for answers or content.
!androjoin	- Bot joins your current voice channel.
!androleave	- Bot leaves the voice channel.

### License
This project is licensed under the MIT License. Contributions are welcome!