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
    DEBUG_MODE, BOX_COLOR
)


def main():
    # 초기화
    hand_tracker = HandTracker()
    gesture_recognizer = GestureRecognizer()
    mouse_controller = MouseController()

    # 스켈레톤 창 설정
    # 스켈레톤 창 설정
    cv2.namedWindow('Hand Control', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Hand Control', SKELETON_WIDTH, SKELETON_HEIGHT)

    # 윈도우 우측 하단에 고정
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT
    window_x = screen_width - SKELETON_WIDTH - 20  # 우측에서 20픽셀 여백
    window_y = screen_height - SKELETON_HEIGHT - 40  # 하단에서 40픽셀 여백

    # 윈도우 위치 설정
    cv2.moveWindow('Hand Control', window_x, window_y)

    # 윈도우를 항상 최상위로 설정
    cv2.setWindowProperty('Hand Control', cv2.WND_PROP_TOPMOST, 1)

    try:
        while True:
            # 웹캠 프레임 획득
            webcam_frame = hand_tracker.get_frame()
            if webcam_frame is None:
                continue

            # 스켈레톤 표시용 캔버스
            skeleton_display = np.zeros((SKELETON_HEIGHT, SKELETON_WIDTH, 3), dtype=np.uint8)

            # 단일 바운딩 박스 그리기
            cv2.rectangle(skeleton_display,
                         (BOX_PADDING, BOX_PADDING),
                         (SKELETON_WIDTH - BOX_PADDING, SKELETON_HEIGHT - BOX_PADDING),
                         BOX_COLOR, BOX_THICKNESS)

            # 핸드 트래킹 수행
            results = hand_tracker.process_frame(webcam_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # gesture 변수 초기화
                    gesture = None
                    position = None

                    # 세 손가락 스크롤 체크
                    if gesture_recognizer.check_scroll_up(hand_landmarks):
                        pyautogui.scroll(120)  # 위로 스크롤
                    elif gesture_recognizer.check_scroll_down(hand_landmarks):
                        pyautogui.scroll(-120)  # 아래로 스크롤
                    # 검지 손가락 포즈 확인
                    elif gesture_recognizer.check_index_finger_up(hand_landmarks):
                        # 제스처 감지 및 처리
                        gesture, position = gesture_recognizer.update_gesture_state(hand_landmarks)

                        if gesture:
                            screen_x = position[0] * SCREEN_WIDTH
                            screen_y = position[1] * SCREEN_HEIGHT

                            if gesture == "SELECT":
                                mouse_controller.select(screen_x, screen_y)
                            elif gesture == "CLICK":
                                mouse_controller.click(screen_x, screen_y)
                            elif gesture == "DRAG":
                                mouse_controller.start_drag(screen_x, screen_y)
                            elif gesture == "DROP":
                                mouse_controller.end_drag(screen_x, screen_y)
                        else:
                            # 기본 마우스 이동
                            mouse_controller.move_mouse(hand_landmarks.landmark[8])

                    # 스켈레톤 그리기
                    hand_tracker.draw_landmarks(skeleton_display, hand_landmarks)

                    # 현재 상태 표시
                    current_area = gesture if gesture else "POINTING" if gesture_recognizer.check_index_finger_up(
                        hand_landmarks) else "NONE"
                    cv2.putText(skeleton_display, current_area,
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