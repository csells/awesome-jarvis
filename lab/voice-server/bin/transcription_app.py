"""Minimal transcription worker: no synthesis or model-management routes."""
from fastapi import FastAPI

def create_app(transcribe,model,lifespan=None):
    app=FastAPI(lifespan=lifespan,docs_url=None,redoc_url=None)
    app.add_api_route('/v1/audio/transcriptions',transcribe,methods=['POST'])
    @app.get('/health')
    async def health():return {'ok':True,'stt_model':model}
    return app
