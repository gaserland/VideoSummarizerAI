# src/export/export_manager.py
from typing import List, Dict, Any
from .audio_exporter import AudioExporter
from .transcript_exporter import TranscriptExporter
from .keyframe_exporter import KeyframeExporter
from .summary_exporter import SummaryExporter

class ExportManager:
    def __init__(self):
        self.exporters = {
            'audio': AudioExporter(),
            'transcript': TranscriptExporter(),
            'keyframes': KeyframeExporter(),
            'summary': SummaryExporter()
        }
    
    def selective_export(self, components: List[str], format_options: Dict, output_dir: str) -> Dict[str, str]:
        """Export selected components in specified formats"""
        results = {}
        
        for component in components:
            if component in self.exporters:
                try:
                    export_path = self.exporters[component].export(
                        format_options.get(component, {}),
                        output_dir
                    )
                    results[component] = export_path
                except Exception as e:
                    results[component] = f"Error: {str(e)}"
                    
        return results
    
    def create_combined_report(self, export_results: Dict, metadata: Dict) -> str:
        """Create a comprehensive report of all exports"""
        # Implementation here
        pass
