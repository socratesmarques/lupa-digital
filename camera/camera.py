import platform
import cv2


class CameraVF0780:
    def __init__(
        self,
        index=0,
        width=1280,
        height=720,
        fps=30,
        buffer_size=1,
        prefer_mjpg=True,
    ):
        self.index = index
        self.width_requested = width
        self.height_requested = height
        self.fps_requested = fps

        # Em Linux/Orange Pi, V4L2 é o backend mais apropriado para webcam UVC.
        if platform.system().lower() == "linux":
            self.cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
        else:
            self.cap = cv2.VideoCapture(index)

        if not self.cap.isOpened():
            return

        if prefer_mjpg:
            self.cap.set(
                cv2.CAP_PROP_FOURCC,
                cv2.VideoWriter_fourcc(*"MJPG")
            )

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

        try:
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
        except Exception:
            pass

    def is_opened(self):
        return self.cap.isOpened()

    def read(self):
        return self.cap.read()

    def release(self):
        if self.cap is not None:
            self.cap.release()

    def info(self):
        if not self.cap.isOpened():
            return {}

        fourcc_int = int(self.cap.get(cv2.CAP_PROP_FOURCC))
        fourcc = "".join(
            chr((fourcc_int >> 8 * i) & 0xFF)
            for i in range(4)
        ).strip("\x00")

        return {
            "width": int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": float(self.cap.get(cv2.CAP_PROP_FPS)),
            "fourcc": fourcc or "desconhecido",
        }
