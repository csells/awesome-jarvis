# Pocket voice catalog preview

A static, mobile-friendly catalog dropdown with audio samples. This is a staged review app, not a live speech-generation client.

The catalog builder reads the pinned Pocket checkout's predefined voices and adds the two custom profiles. Reference recordings are cached locally; gated references remain listed with an explicit unavailable message. No model downloads or private profiles are included here.

```sh
python -m pip install huggingface-hub
python build_voice_catalog.py --pocket-source /path/to/pocket-tts
python -m http.server 8090 --bind 127.0.0.1
```

Supply your own authorized `alfred.wav`, `other-voice.wav` and `realtime.wav` samples beside `index.html`, or adapt the page/custom catalog entries to your profiles. Do not publish private recordings, credentials or model caches. Built-in reference samples are distinct from generated output. Authenticate Hugging Face separately when access to gated references is needed; the script does not embed credentials.

Validation: 29 options (27 built-in and two custom) in the tested pinned version; mobile selection and sample playback verified. Five reference samples required additional Hugging Face access. The candidate synthesis backend currently has the two custom profiles installed; browsing all reference samples does not establish that all voices are installed for synthesis.
