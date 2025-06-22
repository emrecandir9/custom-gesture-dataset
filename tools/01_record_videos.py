import cv2
import time
from pathlib import Path

# --- Path Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATASET_ROOT = PROJECT_ROOT / "dataset"

# --- General Configuration ---
GESTURE_TYPES = ["hand", "body"]
GESTURES = [
    "up", "down", "right", "left", "further", "closer",
    "land", "take_off", "photo", "video", "video_pause",
    "emergency", "follow", "palm", "no_class"
]

# --- Camera and Video Settings ---
CAM_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30
CODEC = 'MJPG'  # Using the more compatible codec

def select_from_list(options, prompt_message):
    """Generic function to prompt user to select an item from a list."""
    print(prompt_message)
    for i, option in enumerate(options, 1):
        print(f"  {i}: {option}")
    
    while True:
        try:
            choice = int(input(f"Enter your choice (1-{len(options)}): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    """
    Main function to run the interactive video recording process.
    """
    print("--- Gesture Video Recorder ---")
    
    gesture_type = select_from_list(GESTURE_TYPES, "\nSelect the gesture type:")
    gesture_name = select_from_list(GESTURES, "\nSelect the gesture to record:")

    output_dir = DATASET_ROOT / "videos" / gesture_type / gesture_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{time.strftime('%Y%m%d_%H%M%S')}.avi"
    output_path = output_dir / filename
    
    print(f"\nOutput directory: {output_dir}")
    print(f"Video will be saved as: {filename}")

    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        print(f"\nError: Could not open camera with index {CAM_INDEX}.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    fourcc = cv2.VideoWriter_fourcc(*CODEC)
    out = cv2.VideoWriter(str(output_path), fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
    
    if not out.isOpened():
        print("\nERROR: Could not open VideoWriter. Check if the codec is supported.")
        cap.release()
        return

    print("\nStarting camera. Press 'R' to start/stop recording. Press 'Q' to quit.")
    is_recording = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        if is_recording:
            cv2.circle(frame, (30, 30), 15, (0, 0, 255), -1)
        else:
            cv2.circle(frame, (30, 30), 15, (128, 128, 128), -1)

        cv2.imshow('Webcam - Press R to Record, Q to Quit', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            if is_recording:
                print("Stopping recording and saving file...")
            break
        elif key == ord('r'):
            is_recording = not is_recording
            status = "Started" if is_recording else "Stopped"
            print(f"Recording {status}!")

        if is_recording:
            out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"\nVideo successfully saved to: {output_path}")
    print("Exiting.")

if __name__ == '__main__':
    main()