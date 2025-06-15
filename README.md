## Voice Agent Framework
A flexible, modular Python framework to build voice-activated assistants by mixing and matching any STT (Speech-to-Text), TTS (Text-to-Speech), and LLM (Large Language Model) backends, whether it be open source or proprietary.

## Features

✔️ **Modular backend swapping** — Easily swap STT, TTS, and LLM providers without changing core logic.<br>
✔️ **Supports local and cloud providers** — Mix offline open-source providers with cloud APIs in a single pipeline.<br>
✔️ **Wake word activation** — Trigger recording hands-free using configurable wake words via Porcupine.<br>
✔️ **Start/stop recording tones** — Audible tones signal when recording starts and stops, with automatic silence detection.<br>

## Providers

A variety of STT, TTS, and LLM providers are supported out of the box, allowing you to experiment with both local and cloud-based models to match different use cases.

Supported provider types:
- **🗣️ Speech-to-Text (STT):** Whisper, Silero
- **💬 Large Language Model (LLM):** Gemini
- **🔊 Text-to-Speech (TTS):** ElevenLabs, Silero, Piper, Gemini

For detailed information on each provider — including features, usage notes, and recommendations — check the [full provider reference](PROVIDERS.md).

## Usage

1. Clone the repo
```bash
git clone git@github.com:b-smyers/voice-agent-framework.git
cd voice-agent-framework
```
2. Create Python 3.10 environment
```bash
python3.10 -m venv venv/
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Configure a custom Agent in `main.py` by swapping out different providers (optional)
    - Check out the [Provider Reference!](PROVIDERS.md)
5. Set environment variables in `.env`
    - `cp .env-sample .env`
    - The defualt Agent configuration requires a [Picovoice](https://picovoice.ai/) and [Gemini](https://aistudio.google.com/apikey) API key, edit `.env` with your API keys. This guide assumes you have access to both.
6. Run the application
```bash
python main.py
```
7. *Presto!* After successful setup, you can now use your Assistant:
    - Say the wake word: **"ok agent"**.
    - Wait for the **start tone**, which means the microphone is listening.
    - Ask your question naturally.
    - When you stop speaking, the system will detect silence and play a **stop tone**.
    - After processing your request, the Assistant will reply using text-to-speech.

> [!NOTE] 
> The recording stays open while you're speaking. If there’s background noise or if you don't pause clearly, it may stay active longer than expected.
