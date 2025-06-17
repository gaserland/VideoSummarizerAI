# src/utils/memory_manager.py
import gc
import psutil
import numpy as np
from typing import Generator, Any

class MemoryManager:
    def __init__(self, max_memory_usage: float = 0.8):
        self.max_memory_usage = max_memory_usage
        self.total_memory = psutil.virtual_memory().total
        
    def chunk_video_processing(self, video_path: str, chunk_duration: int = 60) -> Generator:
        """Process video in memory-efficient chunks"""
        # Implementation for chunked processing
        pass
    
    def memory_efficient_frame_extraction(self, video_path: str) -> Generator[np.ndarray, None, None]:
        """Extract frames without loading entire video into memory"""
        # Implementation here
        pass
    
    def cleanup_memory(self):
        """Force garbage collection and memory cleanup"""
        gc.collect()
        if hasattr(torch, 'cuda') and torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def monitor_memory_usage(self) -> Dict[str, float]:
        """Monitor current memory usage"""
        memory = psutil.virtual_memory()
        return {
            'used_percent': memory.percent,
            'available_gb': memory.available / (1024**3),
            'used_gb': memory.used / (1024**3)
        }
