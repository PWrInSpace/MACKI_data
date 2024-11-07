import cv2
import os

def convert_mp4_to_webm(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error opening video file {input_path}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

def main():
    os.chdir('data')
    workspace = os.getcwd()
    for root, dirs, files in os.walk(workspace):
        for file in files:
            if file.endswith('.mp4'):
                input_path = os.path.join(root, file)
                output_path = os.path.splitext(input_path)[0] + '.webm'
                if not os.path.exists(output_path):
                    print(f"Converting {input_path} to {output_path}")
                    convert_mp4_to_webm(input_path, output_path)
                else:
                    print(f"File {output_path} already exists, skipping conversion.")

if __name__ == "__main__":
    main()