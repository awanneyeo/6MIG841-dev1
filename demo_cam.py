import cv2
import sys
import os

# --- chemins -----------------------------------------------------------
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(SCRIPT_DIR, "hand_landmarker.task")
CODE_DIR    = os.path.join(SCRIPT_DIR, "code")
LAB1_CODE   = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "Lab1", "code"))

sys.path.insert(0, CODE_DIR)
sys.path.insert(0, LAB1_CODE)

# --- config ------------------------------------------------------------
from ihr_ros import config as ihr_config
cfg = ihr_config.load()["devoir1"]

# --- mediapipe ---------------------------------------------------------
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- detection ---------------------------------------------------------
from thumb_detector import ThumbCounter, count_thumbs_up

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17),
]

def draw_skeleton(frame, landmarks, w, h, pouce_leve):
    color_bone  = (0, 255, 0) if pouce_leve else (0, 180, 180)
    color_joint = (0, 0, 255)
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, pts[a], pts[b], color_bone, 2)
    for pt in pts:
        cv2.circle(frame, pt, 4, color_joint, -1)

def main():
    counter = ThumbCounter(cfg)

    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=int(cfg["max_num_hands"]),
        min_hand_detection_confidence=float(cfg["min_detection_confidence"]),
        min_hand_presence_confidence=float(cfg["min_detection_confidence"]),
        min_tracking_confidence=float(cfg["min_tracking_confidence"]),
    )
    detector = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(int(cfg.get("camera_index", 0)))
    if not cap.isOpened():
        print("Erreur : webcam inaccessible.")
        return

    print("=== DEMO POUCES ===  q pour quitter")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
        )
        result = detector.detect(mp_image)

        raw_count = 0
        verdicts  = []

        if result.hand_landmarks:
            raw_count, verdicts = count_thumbs_up(
                result.hand_landmarks, image_width=w, image_height=h
            )
            for i, hand_lm in enumerate(result.hand_landmarks):
                pouce_leve = i < len(verdicts) and verdicts[i].is_up
                draw_skeleton(frame, hand_lm, w, h, pouce_leve)

        stable = counter.update(raw_count)

        # --- HUD -------------------------------------------------------
        couleur = (0, 255, 0) if stable > 0 else (200, 200, 200)
        cv2.putText(frame, f"Pouces leves : {stable}",
                    (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, couleur, 3, cv2.LINE_AA)
        cv2.putText(frame, f"(brut: {raw_count}  fenetre: {cfg['debounce_frames']} trames)",
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1, cv2.LINE_AA)

        for i, v in enumerate(verdicts):
            cv2.putText(frame, f"Main {i+1}: {v.explain()}",
                        (20, 120 + i * 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 1, cv2.LINE_AA)

        cv2.imshow("Demo Devoir 1 - Pouces", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
