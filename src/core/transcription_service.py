from typing import Dict


class TranscriptionService:
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        self.thai_model = load_thai_stt_model()
        
    def transcribe_english(self, audio_path: str) -> Dict:
        """Transcribe English audio with timestamps"""
        
    def transcribe_thai(self, audio_path: str) -> Dict:
        """Transcribe Thai audio with timestamps"""
        
    def post_process_transcript(self, transcript: Dict) -> Dict:
        """Clean and format transcription"""