# src/utils/parallel_processor.py
import multiprocessing as mp
import torch
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Callable, Any

class ParallelProcessor:
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or mp.cpu_count()
        self.use_gpu = torch.cuda.is_available()
    
    def process_video_chunks(self, video_chunks: List, process_func: Callable) -> List[Any]:
        """Process video chunks in parallel"""
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(process_func, video_chunks))
        return results
    
    def async_multimodal_processing(self, audio_path: str, video_path: str) -> Dict:
        """Process audio, video, and text extraction simultaneously"""
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all tasks
            audio_future = executor.submit(self._process_audio, audio_path)
            video_future = executor.submit(self._process_video, video_path)
            transcript_future = executor.submit(self._process_transcript, audio_path)
            
            # Collect results
            return {
                'audio': audio_future.result(),
                'video': video_future.result(),
                'transcript': transcript_future.result()
            }
