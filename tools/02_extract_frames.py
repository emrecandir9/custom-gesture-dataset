import cv2
import uuid
from pathlib import Path
from tqdm import tqdm

# --- Path Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
VIDEOS_DIR = PROJECT_ROOT / "dataset" / "videos"
PHOTOS_DIR = PROJECT_ROOT / "dataset" / "photos"

# --- Frame Extraction Settings ---
TARGET_FPS = 2.0
IMAGE_FORMAT = ".jpg"

def extract_frames(video_path: Path, output_dir: Path):
    """
    Extracts frames from a single video file.
    """
    frames_saved = 0
    try:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return 0

        video_fps = cap.get(cv2.CAP_PROP_FPS)
        if video_fps == 0:
            return 0
            
        frame_skip = int(video_fps / TARGET_FPS) if TARGET_FPS > 0 else 1
        output_dir.mkdir(parents=True, exist_ok=True)
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break 
            
            if frame_count % frame_skip == 0:
                unique_id = uuid.uuid4()
                output_file = output_dir / f"frame_{unique_id}{IMAGE_FORMAT}"
                cv2.imwrite(str(output_file), frame)
                frames_saved += 1
            
            frame_count += 1
            
        cap.release()
        return frames_saved

    except Exception as e:
        print(f"\nAn error occurred while processing {video_path.name}: {e}")
        return 0

def main():
    print("--- Video to Frame Extractor ---")
    
    if not VIDEOS_DIR.exists():
        print(f"Error: Videos directory not found at '{VIDEOS_DIR}'")
        return
        
    video_files = list(VIDEOS_DIR.rglob("*.avi"))
    if not video_files:
        print("No .avi videos found to process.")
        return

    print(f"Found {len(video_files)} videos to process.")
    total_frames_extracted = 0
    
    for video_path in tqdm(video_files, desc="Processing videos"):
        relative_path = video_path.relative_to(VIDEOS_DIR)
        output_dir = PHOTOS_DIR / relative_path.parent
        
        num_saved = extract_frames(video_path, output_dir)
        if num_saved == 0:
            print(f"\nWARNING: No frames were extracted from {video_path.name}. The video file may be empty or have a codec issue.")
        total_frames_extracted += num_saved
        
    print(f"\n--- All videos processed! ---")
    print(f"Total frames extracted across all videos: {total_frames_extracted}")


if __name__ == '__main__':
    main()