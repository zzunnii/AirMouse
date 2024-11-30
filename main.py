import cv2
import numpy as np
from PIL import ImageGrab
import time

from modules.hand_tracker import HandTracker
from modules.gesture_recognizer import GestureRecognizer
from modules.mouse_controller import MouseController
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT


def main():
    # 모듈 초기화
    hand_tracker = HandTracker()
    gesture_recognizer = GestureRecognizer()
    mouse_controller = MouseController()

    # 스켈레톤 창 설정 (작은 크기로)
    cv2.namedWindow('Hand Skeleton', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Hand Skeleton', 300, 200)  # 더 작게 조절 가능

    try:
        while True:

            # 웹캠 프레임 획득
            webcam_frame = hand_tracker.get_frame()
            if webcam_frame is None:
                continue

            # 작은 크기로 조정된 스켈레톤 표시용 캔버스
            skeleton_display = np.zeros((200, 300, 3), dtype=np.uint8)

            # 핸드 트래킹 수행
            results = hand_tracker.process_frame(webcam_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 제스처 인식 및 처리
                    gesture = gesture_recognizer.update_gesture_state(hand_landmarks)

                    # 엔터키를 위한 주먹 제스처 감지
                    if gesture_recognizer.detect_fist_and_release(hand_landmarks):
                        mouse_controller.press_enter()

                    if gesture == "CLICK":
                        mouse_controller.click()
                    elif gesture == "SCROLL":
                        scroll_amount = gesture_recognizer.get_scroll_amount(hand_landmarks)
                        if scroll_amount != 0:
                            mouse_controller.scroll(scroll_amount)
                    else:
                        gesture_recognizer.reset_scroll_state()
                        cursor_x, cursor_y = mouse_controller.move_mouse(hand_landmarks.landmark[8])

                    # 스켈레톤만 표시
                    hand_tracker.draw_landmarks(skeleton_display, hand_landmarks)

                    # 현재 모드 표시 (선택적)
                    mode_text = "SCROLL" if gesture == "SCROLL" else "MOUSE"
                    cv2.putText(skeleton_display, mode_text, (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # 스켈레톤 창 업데이트
            cv2.imshow('Hand Skeleton', skeleton_display)

            # ESC 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        # 리소스 정리
        hand_tracker.cleanup()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()