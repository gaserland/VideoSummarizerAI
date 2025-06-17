from typing import Dict, List
import numpy as np

class VideoProcessor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.metadata = {}
        
    def extract_audio(self) -> np.ndarray:
        """Extract audio using FFmpeg
    
        Returns:
            np.ndarray: The extracted audio data as a numpy array
        """
        # Load settings from yaml file
        import yaml

        with open('config/settings.yaml', 'r') as f:
            settings = yaml.safe_load(f)

        # Get supported video formats and allowed extensions
        supported_formats = settings['video']['supported_formats']
        # Check if the given video_path has a format that is supported, else throw an exception or return error message.
        file_extension = '.' + self.video_path.split('.')[-1].lower()
        if file_extension not in supported_formats:
            raise ValueError(f"Unsupported video format: {file_extension}. Supported formats are {supported_formats}")

        # Get audio extraction parameters
        sample_rate = settings['audio']['sample_rate']
        extraction_format = settings['audio']['extraction_format']

        # Use FFmpeg to extract audio with the specified sample rate and output format.
        import subprocess

        command = [
            'ffmpeg',
            '-i', self.video_path,
            '-ar', str(sample_rate),
            '-acodec', 'pcm_s16le',
            '-f', extraction_format.lower(),
            'pipe:'
        ]

        try:
            # Run the FFmpeg command and capture output
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.audio_data = np.frombuffer(result.stdout, dtype=np.int16)
            self.sample_rate = sample_rate
            return self.audio_data
        
        except Exception as e:
            print(f"Error extracting audio: {e}")
            raise RuntimeError(f"Audio extraction failed: {str(e)}")
        
    def extract_frames(self, interval: float = 1.0) -> List[np.ndarray]:
        """Extract frames at specified intervals
    
        Args:
            interval (float): Time interval between frames in seconds (default: 1.0)
            
        Returns:
            List[np.ndarray]: List of extracted frames as numpy arrays
        """
        import cv2
        import os
        
        # Check if the file exists
        if not os.path.isfile(self.video_path):
            raise FileNotFoundError(f"Video file not found: {self.video_path}")
        
        # Open the video file
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video file: {self.video_path}")
        
        # Get video properties
        if not hasattr(self, 'fps') or not hasattr(self, 'duration'):
            info = self.get_video_info()
            fps = info['fps']
            duration = info['duration']
        else:
            fps = self.fps
            duration = self.duration
        
        # Calculate frame interval in terms of frame count
        frame_interval = int(fps * interval)
        
        frames = []
        frame_count = 0
        
        try:
            while True:
                # Set frame position
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
                
                # Read the frame
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Convert to RGB (OpenCV uses BGR)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame_rgb)
                
                # Update frame count
                frame_count += frame_interval
                
                # Check if we've reached the end of the video
                if frame_count >= fps * duration:
                    break
                    
        except Exception as e:
            print(f"Error extracting frames: {e}")
            raise
        finally:
            # Release the video capture object
            cap.release()
        
        print(f"Extracted {len(frames)} frames at {interval} second intervals")
        return frames
        
    def get_video_info(self) -> Dict:
        """Get video metadata (duration, fps, resolution, codec info)
    
        Returns:
            Dict: A dictionary containing video metadata including:
                - duration (float): Length of video in seconds
                - fps (float): Frames per second
                - resolution (tuple): Width and height in pixels (width, height)
                - codec (str): Video codec information
                - bit_rate (int): Video bit rate
                - size (int): File size in bytes
                - audio_codec (str): Audio codec if available
                - audio_channels (int): Number of audio channels
        """
        import subprocess
        import json
        import os
        
        try:
            # Prepare FFprobe command to extract video information in JSON format
            command = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                self.video_path
            ]
            
            # Run FFprobe and capture output
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                raise ValueError(f"FFprobe failed: {result.stderr}")
                
            # Parse the JSON output
            probe_data = json.loads(result.stdout)
            
            # Initialize variables
            video_stream = None
            audio_stream = None
            
            # Find video and audio streams
            for stream in probe_data.get('streams', []):
                if stream.get('codec_type') == 'video' and not video_stream:
                    video_stream = stream
                elif stream.get('codec_type') == 'audio' and not audio_stream:
                    audio_stream = stream
            
            # Extract video information
            if not video_stream:
                raise ValueError("No video stream found in the file")
                
            # Get format information
            format_info = probe_data.get('format', {})
            
            # Extract key information
            width = int(video_stream.get('width', 0))
            height = int(video_stream.get('height', 0))
            
            # Calculate fps - handle different formats
            fps_str = video_stream.get('r_frame_rate', '0/0')
            if '/' in fps_str:
                num, den = map(int, fps_str.split('/'))
                fps = num / den if den else 0
            else:
                fps = float(fps_str)
            
            # Extract duration
            duration = float(format_info.get('duration', video_stream.get('duration', 0)))
            
            # File size
            size = int(format_info.get('size', os.path.getsize(self.video_path)))
            
            # Store as instance attributes
            self.fps = fps
            self.duration = duration
            self.resolution = (width, height)
            self.frame_count = int(fps * duration) if fps and duration else 0
            self.video_codec = video_stream.get('codec_name')
            
            # Create info dictionary
            video_info = {
                'duration': duration,
                'fps': fps,
                'resolution': (width, height),
                'frame_count': self.frame_count,
                'codec': video_stream.get('codec_name'),
                'bit_rate': int(format_info.get('bit_rate', 0)),
                'size': size,
                'path': self.video_path
            }
            
            # Add audio information if available
            if audio_stream:
                self.audio_codec = audio_stream.get('codec_name')
                self.audio_channels = int(audio_stream.get('channels', 0))
                
                video_info.update({
                    'audio_codec': self.audio_codec,
                    'audio_channels': self.audio_channels,
                    'audio_sample_rate': int(audio_stream.get('sample_rate', 0))
                })
            
            return video_info
            
        except Exception as e:
            print(f"Error getting video info: {e}")
            raise RuntimeError(f"Failed to get video information: {str(e)}")
