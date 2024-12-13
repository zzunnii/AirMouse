import cv2
import numpy as np
from modules.hand_tracker import HandTracker
from modules.gesture_recognizer import GestureRecognizer
from modules.mouse_controller import MouseController
from config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    SKELETON_WIDTH, SKELETON_HEIGHT,
    BOX_PADDING, BOX_COLOR, BOX_THICKNESS,
    SKELETON_COLOR
)


def main():
    # 초기화
    hand_tracker = HandTracker()
    gesture_recognizer = GestureRecognizer()
    mouse_controller = MouseController()

    # 스켈레톤 창 설정
    cv2.namedWindow('Hand Skeleton', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Hand Skeleton', SKELETON_WIDTH, SKELETON_HEIGHT)

    try:
        while True:
            # 웹캠 프레임 획득
            webcam_frame = hand_tracker.get_frame()
            if webcam_frame is None:
                continue

            # 스켈레톤 표시용 캔버스
            skeleton_display = np.zeros((SKELETON_HEIGHT, SKELETON_WIDTH, 3), dtype=np.uint8)

            # 바운딩 박스 그리기
            cv2.rectangle(skeleton_display,
                          (BOX_PADDING, BOX_PADDING),
                          (SKELETON_WIDTH - BOX_PADDING, SKELETON_HEIGHT - BOX_PADDING),
                          BOX_COLOR, BOX_THICKNESS)

            # 핸드 트래킹 수행
            results = hand_tracker.process_frame(webcam_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 제스처 인식 및 처리
                    gesture, position = gesture_recognizer.update_gesture_state(hand_landmarks)

                    # 제스처에 따른 동작 처리
                    if gesture == "CLICK":
                        if position:
                            screen_x = position[0] * SCREEN_WIDTH
                            screen_y = position[1] * SCREEN_HEIGHT
                            mouse_controller.click(screen_x, screen_y)

                    elif gesture == "DOUBLE_CLICK":
                        if position:
                            screen_x = position[0] * SCREEN_WIDTH
                            screen_y = position[1] * SCREEN_HEIGHT
                            mouse_controller.double_click(screen_x, screen_y)

                    elif gesture == "DRAG":
                        if position:
                            screen_x = position[0] * SCREEN_WIDTH
                            screen_y = position[1] * SCREEN_HEIGHT
                            mouse_controller.start_drag(screen_x, screen_y)

                    elif gesture == "DROP":
                        if position:
                            screen_x = position[0] * SCREEN_WIDTH
                            screen_y = position[1] * SCREEN_HEIGHT
                            mouse_controller.end_drag(screen_x, screen_y)
                    else:
                        # 기본 마우스 이동
                        mouse_controller.move_mouse(hand_landmarks.landmark[8])

                    # 스켈레톤 그리기
                    hand_tracker.draw_landmarks(skeleton_display, hand_landmarks)

                    # 현재 모드 표시
                    cv2.putText(skeleton_display, gesture if gesture else "MOUSE",
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, SKELETON_COLOR, 1)

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