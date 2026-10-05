from pathlib import Path
r=Path.home()/'code/henryklunaris/hey-jev'
p=r/'siri.py';s=p.read_text();old='if __name__ == "__main__":\n    main()'
assert old in s
s=s.replace(old,'# LAB ONLY: service substitutions and timestamped state evidence.\nimport lab_adapter\nlab_adapter.install(sys.modules[__name__])\n\n'+old)
s=s.replace('if not TS_KEY or not FISH_KEY:', 'if not TS_KEY:').replace('need TYPESAFE_API_KEY and FISH_AUDIO_API_KEY in Keychain or .env','LAB: need TYPESAFE_API_KEY in Keychain or .env')
gate='        if not (OA_KEY or OR_KEY):\n            say("Add an OpenRouter or OpenAI key first.", notify)\n            emit(notify, "Ready", "Dictation needs an OpenRouter or OpenAI key")\n            return\n'
assert gate in s
s=s.replace(gate, '        # LAB: local Whisper dictation does not need cloud credentials.\n')
p.write_text(s)
p=r/'secrets_store.py' ;s=p.read_text();old='return [name for name in KEY_NAMES if name not in OPTIONAL and not get_secret(name)]';assert old in s
p.write_text(s.replace(old,'return [name for name in ("TYPESAFE_API_KEY",) if not get_secret(name)]  # LAB: other services replaced'))
print('Applied lab adapter; TypeSafe classification and action/recorder/UI logic unchanged.')
