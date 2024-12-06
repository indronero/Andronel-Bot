# Andronel - Versatile Discord Bot with AI and Music Capabilities

Andronel is an advanced AI-driven Discord bot that integrates Google Generative AI's **Gemini API** for intelligent chat responses, along with powerful music playback capabilities, voice channel management, and more. It's a feature-rich assistant designed to enhance your Discord experience.

---

## Features

1. **AI Chat Integration with Gemini**
   - Use `/ask` command to get intelligent responses from Google's Gemini AI
   - Automatic handling of long responses by splitting into multiple messages

2. **Music Playback**
   - `/play [song title]`: Instantly play music from YouTube
   - `/pause`: Pause the current track
   - `/resume`: Resume playback

3. **Voice Channel Management**
   - `/androjoin`: Bot joins your current voice channel
   - `/androleave`: Bot leaves the voice channel

4. **Utility Commands**
   - `/hello`: Get a friendly greeting from the bot

---

## Prerequisites

- Python 3.8+  
- **Discord Bot Token** (available from the [Discord Developer Portal](https://discord.com/developers/applications)).  
- **Google Gemini API Key** (get access [here](https://developers.generativeai.google/)).
- FFmpeg (for music playback). Install it from [FFmpeg.org](https://ffmpeg.org/).

---

## Setup

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/andronel.git
   cd andronel

2. Install dependencies:
   ```bash
   pip install discord.py google-generativeai yt-dlp

3. Create an `apikeys.py` file:
   ```bash
   botToken = "YOUR_DISCORD_BOT_TOKEN"
   geminiToken = "YOUR_GEMINI_API_KEY"
   ```
   **Note**: Ensure apikeys.py is listed in `.gitignore` to keep your tokens secure.

4. Run the bot:
   ```bash
   python3 main.py

---

## Commands

| Command | Description |
|---------|-------------|
| `/hello` | Sends a friendly greeting |
| `/ask [question]` | Query Gemini AI for intelligent responses |
| `/androjoin` | Bot joins your current voice channel |
| `/androleave` | Bot leaves the voice channel |
| `/play [song title]` | Play a song from YouTube |
| `/pause` | Pause the current track |
| `/resume` | Resume playback |

---

## Troubleshooting

- Ensure all API keys are correctly set in `apikeys.py`
- Verify you have the latest versions of dependencies
- Check Discord bot permissions and intents

## License

This project is licensed under the MIT License. Contributions are welcome!