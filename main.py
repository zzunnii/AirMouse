import cv2
import numpy as np
import pyautogui

from modules.hand_tracker import HandTracker
from modules.gesture_recognizer import GestureRecognizer
from modules.mouse_controller import MouseController
from config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    SKELETON_WIDTH, SKELETON_HEIGHT,
    BOX_PADDING, BOX_THICKNESS,
    DEBUG_MODE, BOX_COLOR, MOUSEPAD_MARGIN, MOUSEPAD_THICKNESS, MOUSEPAD_COLOR
)


def main():
    # 초기화
    hand_tracker = HandTracker()
    gesture_recognizer = GestureRecognizer()
    mouse_controller = MouseController()

    # 스켈레톤 창 설정
    cv2.namedWindow('Hand Control', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Hand Control', SKELETON_WIDTH, SKELETON_HEIGHT)

    # 윈도우 우측 하단에 고정
    window_x = SCREEN_WIDTH - SKELETON_WIDTH - 20  # 우측에서 20픽셀 여백
    window_y = SCREEN_HEIGHT - SKELETON_HEIGHT - 40  # 하단에서 40픽셀 여백
    cv2.moveWindow('Hand Control', window_x, window_y)

    # 윈도우를 항상 최상위로 설정
    cv2.setWindowProperty('Hand Control', cv2.WND_PROP_TOPMOST, 1)

    try:
        while True:
            # 웹캠 프레임 획득
            webcam_frame = hand_tracker.get_frame()
            if webcam_frame is None:
                continue

            # 프레임 크기 가져오기
            frame_height, frame_width = webcam_frame.shape[:2]

            # 스켈레톤 표시용 캔버스
            skeleton_display = np.zeros((SKELETON_HEIGHT, SKELETON_WIDTH, 3), dtype=np.uint8)

            # 외부 바운딩 박스 그리기
            cv2.rectangle(skeleton_display,
                          (BOX_PADDING, BOX_PADDING),
                          (SKELETON_WIDTH - BOX_PADDING, SKELETON_HEIGHT - BOX_PADDING),
                          BOX_COLOR, BOX_THICKNESS)

            # 내부 마우스패드 영역 그리기
            cv2.rectangle(skeleton_display,
                          (MOUSEPAD_MARGIN, MOUSEPAD_MARGIN),
                          (SKELETON_WIDTH - MOUSEPAD_MARGIN, SKELETON_HEIGHT - MOUSEPAD_MARGIN),
                          MOUSEPAD_COLOR, MOUSEPAD_THICKNESS)

            # 핸드 트래킹 수행
            results = hand_tracker.process_frame(webcam_frame)

            # 제스처 상태 초기화
            gesture = None
            position = None
            status = "NONE"

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 스크롤 체크
                    if gesture_recognizer.check_scroll_up(hand_landmarks):
                        pyautogui.scroll(120)  # 위로 스크롤
                        status = "SCROLL UP"
                    elif gesture_recognizer.check_scroll_down(hand_landmarks):
                        pyautogui.scroll(-120)  # 아래로 스크롤
                        status = "SCROLL DOWN"
                    else:
                        # 제스처 감지 및 처리
                        gesture, position = gesture_recognizer.update_gesture_state(hand_landmarks)

                        if gesture:
                            screen_x = position[0] * SCREEN_WIDTH
                            screen_y = position[1] * SCREEN_HEIGHT

                            if gesture == "CLICK":
                                mouse_controller.click(screen_x, screen_y)
                            elif gesture == "DRAG":
                                mouse_controller.start_drag(screen_x, screen_y)
                            elif gesture == "DROP":
                                mouse_controller.end_drag(screen_x, screen_y)
                            status = gesture
                        else:
                            # 기본 마우스 이동
                            mouse_controller.move_mouse(hand_landmarks.landmark[8])
                            status = "MOVE"

                    # 스켈레톤 그리기
                    hand_tracker.draw_landmarks(skeleton_display, hand_landmarks)

                    # 현재 상태 표시
                    cv2.putText(skeleton_display, status,
                                (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255), 1)

            # 스켈레톤 창 업데이트
            cv2.imshow('Hand Control', skeleton_display)

            # ESC 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        # 리소스 정리
        hand_tracker.cleanup()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()