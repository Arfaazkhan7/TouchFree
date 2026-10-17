import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

EDGE_MARGIN = 0.15
DEAD_ZONE = 0.004
BASE_SPEED = 1.6
KALMAN_PROCESS_N = 1e-3
KALMAN_MEASURE_N = 5e-2

CLICK_DELAY = 0.35
BEND_THRESHOLD = 148
OPEN_THRESHOLD = 162

SCROLL_SPEED = 30
ZOOM_SENSITIVITY = 0.004

SCREENSHOT_DIR = "screenshots"


class KalmanFilter1D:
    def __init__(self, process_noise=KALMAN_PROCESS_N,
                 measure_noise=KALMAN_MEASURE_N):
        self.q = process_noise
        self.r = measure_noise
        self.x = 0.0
        self.p = 1.0
        self.initialized = False

    def update(self, z):
        if not self.initialized:
            self.x = z
            self.initialized = True
            return z
        self.p += self.q
        k = self.p / (self.p + self.r)
        self.x += k * (z - self.x)
        self.p *= (1 - k)
        return self.x


def finger_angle(a, b, c):
    ba = np.array([a.x - b.x, a.y - b.y])
    bc = np.array([c.x - b.x, c.y - b.y])
    cos = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cos, -1, 1)))


def thumb_open(lm):
    return lm[4].x < lm[3].x


def remap(v, margin=EDGE_MARGIN):
    return float(np.clip((v - margin) / (1 - 2 * margin), 0, 1))


class VelocityAdaptor:
    def __init__(self, low=0.002, high=0.04,
                 min_scale=0.7, max_scale=2.4):
        self.low = low
        self.high = high
        self.min_s = min_scale
        self.max_s = max_scale
        self.prev = None

    def scale(self, nx, ny):
        if self.prev is None:
            self.prev = (nx, ny)
            return 1.0
        dx = nx - self.prev[0]
        dy = ny - self.prev[1]
        speed = (dx**2 + dy**2) ** 0.5
        self.prev = (nx, ny)
        t = np.clip((speed - self.low) / (self.high - self.low), 0, 1)
        return self.min_s + t * (self.max_s - self.min_s)


screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.72,
    min_tracking_confidence=0.72
)
mp_draw = mp.solutions.drawing_utils

kf_x = KalmanFilter1D()
kf_y = KalmanFilter1D()
vel = VelocityAdaptor()

cursor_x, cursor_y = screen_w // 2, screen_h // 2

last_click_time = 0
drag_active = False
prev_index_bent = False
prev_middle_bent = False
prev_both_bent = False
prev_three_bent = False
prev_scroll_y = None
prev_zoom_y = None
prev_swipe_y = None

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark
        now = time.time()

        idx_ang = finger_angle(lm[5], lm[6], lm[8])
        mid_ang = finger_angle(lm[9], lm[10], lm[12])
        rng_ang = finger_angle(lm[13], lm[14], lm[16])
        lit_ang = finger_angle(lm[17], lm[18], lm[20])

        index_open = idx_ang > OPEN_THRESHOLD
        middle_open = mid_ang > OPEN_THRESHOLD
        ring_open = rng_ang > OPEN_THRESHOLD
        little_open = lit_ang > OPEN_THRESHOLD

        index_bent = idx_ang < BEND_THRESHOLD
        middle_bent = mid_ang < BEND_THRESHOLD
        ring_bent = rng_ang < BEND_THRESHOLD

        thumb_is_open = thumb_open(lm)

        move_mode = index_open and middle_open and not thumb_is_open and not ring_open and not little_open
        freeze_gesture = thumb_is_open and index_open and middle_open and not ring_open and not little_open
        fist = index_bent and middle_bent and not ring_open and not little_open and not thumb_is_open
        scroll_mode = index_open and not middle_open and not ring_open and not little_open and not thumb_is_open
        zoom_mode = index_open and middle_open and ring_open and not little_open and not thumb_is_open
        taskview_mode = thumb_is_open and index_open and not middle_open and not ring_open and not little_open

        if fist and not drag_active:
            pyautogui.mouseDown()
            drag_active = True
        if drag_active and not fist:
            pyautogui.mouseUp()
            drag_active = False

        if scroll_mode:
            y = lm[8].y
            if prev_scroll_y is not None:
                dy = prev_scroll_y - y
                if abs(dy) > DEAD_ZONE:
                    pyautogui.scroll(int(dy * SCROLL_SPEED * 100))
            prev_scroll_y = y
        else:
            prev_scroll_y = None

        if zoom_mode:
            y = lm[8].y
            if prev_zoom_y is not None:
                dy = prev_zoom_y - y
                if dy > ZOOM_SENSITIVITY:
                    pyautogui.keyDown("ctrl"); pyautogui.scroll(60); pyautogui.keyUp("ctrl")
                elif dy < -ZOOM_SENSITIVITY:
                    pyautogui.keyDown("ctrl"); pyautogui.scroll(-60); pyautogui.keyUp("ctrl")
            prev_zoom_y = y
        else:
            prev_zoom_y = None

        if taskview_mode:
            y = lm[8].y
            if prev_swipe_y is not None and (prev_swipe_y - y) > 0.05:
                pyautogui.hotkey("win", "tab")
            prev_swipe_y = y
        else:
            prev_swipe_y = None

        if (move_mode or drag_active) and not freeze_gesture:
            raw_x = lm[8].x
            raw_y = lm[8].y

            nx = remap(raw_x)
            ny = remap(raw_y)

            dx_raw = nx - (cursor_x / screen_w)
            dy_raw = ny - (cursor_y / screen_h)
            if abs(dx_raw) < DEAD_ZONE and abs(dy_raw) < DEAD_ZONE:
                pass
            else:
                spd = vel.scale(nx, ny)

                target_x = kf_x.update(nx * screen_w * spd * BASE_SPEED
                                        + cursor_x * (1 - spd * BASE_SPEED))
                target_y = kf_y.update(ny * screen_h * spd * BASE_SPEED
                                        + cursor_y * (1 - spd * BASE_SPEED))

                cursor_x = int(np.clip(target_x, 0, screen_w - 1))
                cursor_y = int(np.clip(target_y, 0, screen_h - 1))

                pyautogui.moveTo(cursor_x, cursor_y)

        both_bent = index_bent and middle_bent and thumb_is_open
        if prev_both_bent and not both_bent and now - last_click_time > CLICK_DELAY:
            pyautogui.doubleClick()
            last_click_time = now
        prev_both_bent = both_bent

        left_gesture = thumb_is_open and middle_open and not ring_open and not little_open
        if left_gesture and prev_index_bent and not index_bent:
            if now - last_click_time > CLICK_DELAY:
                pyautogui.click()
                last_click_time = now

        right_gesture = thumb_is_open and index_open and not ring_open and not little_open
        if right_gesture and prev_middle_bent and not middle_bent:
            if now - last_click_time > CLICK_DELAY:
                pyautogui.rightClick()
                last_click_time = now

        screenshot_pose = thumb_is_open and index_open and middle_open and ring_open and not little_open
        three_bent = index_bent and middle_bent and ring_bent
        if screenshot_pose and prev_three_bent and not three_bent:
            fname = f"{SCREENSHOT_DIR}/screenshot_{int(now)}.png"
            pyautogui.screenshot().save(fname)
            print(f"📸 Screenshot saved → {fname}")
        prev_three_bent = three_bent

        prev_index_bent = index_bent
        prev_middle_bent = middle_bent

        mp_draw.draw_landmarks(
            frame,
            result.multi_hand_landmarks[0],
            mp_hands.HAND_CONNECTIONS
        )

        active = []
        if move_mode:      active.append("MOVE")
        if freeze_gesture: active.append("FREEZE")
        if drag_active:    active.append("DRAG")
        if scroll_mode:    active.append("SCROLL")
        if zoom_mode:      active.append("ZOOM")
        if taskview_mode:  active.append("TASK VIEW")
        label = " | ".join(active) if active else "—"
        cv2.putText(frame, label, (12, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 220, 120), 2)

    cv2.imshow("Touch-Free Control [ESC = quit]", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()