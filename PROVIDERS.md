# Overview
## STT (Speech-to-Text) Providers
| Provider                | Link                                                | Source         | Notes                                             |
|-------------------------|-----------------------------------------------------|----------------|---------------------------------------------------|
| [Whisper](#whisper-stt) | [GitHub](https://github.com/openai/whisper)         | Open-source    | OpenAI, high accuracy, broad language support     |
| [Silero](#silero-stt)   | [GitHub](https://github.com/snakers4/silero-models) | Open-source    | Lightweight, medium accuracy, ok language support |

### LLM (Large Language Model) Providers
| Provider                | Link                                                                   | Source         | Notes                                   |
|-------------------------|------------------------------------------------------------------------|----------------|-----------------------------------------|
| [Gemini](#gemini-llm)   | [Google Gemini](https://ai.google.dev/gemini-api/docs/text-generation) | Closed-source  | Cloud API, free tier, fast              |
| [ChatGPT](#chatgpt-llm) | [ChatGPT API](https://openai.com/api/)                                 | Closed-source  | Cloud API, paid, fast                   |

## TTS (Text-to-Speech) Providers
| Provider                      | Link                                                                     | Source         | Notes                                 |
|-------------------------------|--------------------------------------------------------------------------|----------------|---------------------------------------|
| [ElevenLabs](#elevenlabs-tts) | [GitHub](https://github.com/elevenlabs/elevenlabs-python)                | Closed-source  | Cloud API, high-quality, free tier    |
| [Silero](#silero-tts)         | [GitHub](https://github.com/snakers4/silero-models)                      | Open-source    | Runs locally, fast, low quality       |
| [Piper](#piper-tts)           | [GitHub](https://github.com/rhasspy/piper)                               | Open-source    | Runs locally, fast, medium quality    |
| [Gemini](#gemini-tts)         | [Google Gemini](https://ai.google.dev/gemini-api/docs/speech-generation) | Closed-source  | Cloud API, high quality, free-for-now |

# STT (Speech-to-Text)
## Whisper STT

| Source        | Usage       | Quality | Speed  | Pricing  |
|---------------|-------------|---------|--------|----------|
| Open-source   | Self hosted | High*   | Medium | Free     |

**Additional Notes**

Whisper STT is an efficient speech-to-text model that excels at transcribing short or long sentences, but struggles with short inputs. *[Whisper tends to hallucinate](https://arxiv.org/html/2402.08021v2) or generate repetitive phrases when given very short or silent inputs, as it is optimized for longer, continuous speech.

## Silero STT

| Source        | Usage       | Quality | Speed  | Pricing  |
|---------------|-------------|---------|--------|----------|
| Open-source   | Self hosted | Medium  | High   | Free     |

**Additional Notes**

Silero STT's default output can be a little messy and neglect to add spaces between words, some of theses occurences can be fixed with the text enhancement model on the original transcript. This is the default behavior. The model also struggles to correctly transcribe acronyms.

# LLM (Large Language Model)
## Gemini LLM

| Source        | Usage       | Quality | Speed  | Pricing  |
|---------------|-------------|---------|--------|----------|
| Closed-source | Cloud API   | High    | High   | Freemium |

**Additional Notes**

You can experiment with the Gemini LLM [here](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash). The Gemini LLM is capable of using custom built tools, provided as Python functions, but this comes at a cost. By default, Gemini can use Google Search for grounding, but support for Google Search AND custom tools/functions is not supported as of now.

### ChatGPT LLM

| Source        | Usage       | Quality | Speed  | Pricing  |
|---------------|-------------|---------|--------|----------|
| Closed-source | Cloud API   | High    | High   | Paid     |

**Additional Notes**

Unfortunately, free testing is limited to what is available on the official ChatGPT website. By default, the ChatGPTLLMClient uses `gpt-4.1-nano`, an incredibly cheap and fast model. Tool usage is supported by ChatGPT but has not yet been integrated in this repo.

## TTS (Text-to-Speech)
### ElevenLabs TTS

| Source        | Usage       | Quality | Speed  | Pricing  |
|---------------|-------------|---------|--------|----------|
| Closed-source | Cloud API   | High    | High   | Freemium |

**Additional Notes**

ElevenLabs requires mpv for voice streaming (the default method):
```bash
sudo apt install mpv
```

## Silero TTS

| Source        | Usage       | Quality | Speed  | Pricing  |
|---------------|-------------|---------|--------|----------|
| Open-source   | Self hosted | Low     | High   | Free     |

**Additional Notes**

Samples for english speaking models can be found [here](https://oobabooga.github.io/silero-samples/index.html).

## Piper TTS

| Source        | Usage       | Quality | Speed  | Pricing  |
|---------------|-------------|---------|--------|----------|
| Open-source   | Self hosted | Medium  | High   | Free     |

**Additional Notes**

You can sample and download Piper voice models [here](https://rhasspy.github.io/piper-samples/). `English (English, United States) hfc_female` is recommended for its clear articulation on a wide variety of english text, making it suitable for general-purpose conversational agents ([link](https://rhasspy.github.io/piper-samples/#en_US-hfc_female-medium)). Make sure to download both the `.onnx` and `.onnx.json` file and place them in the same directory before passing the path to the PiperTTSClient.

## Gemini TTS

| Source        | Usage       | Quality | Speed  | Pricing  |
|---------------|-------------|---------|--------|----------|
| Closed-source | Cloud API   | High    | Slow   | Freemium |

**Additional Notes**

You can expirement with the predefined Gemini TTS models [here](https://aistudio.google.com/generate-speech). The Gemini TTS is current experimental and for the time being, free within a quota, but Google made a [notice](https://ai.google.dev/gemini-api/docs/pricing#gemini-2.5-flash-preview-tts) that this could change at any moment.
