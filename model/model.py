import cv2
from random import randint

class MultiObjectTracker:
    def __init__(self, video_path, tracker_type, resize_dim=(720, 640)):
        self.video_path = video_path
        self.tracker_type = tracker_type
        self.resize_dim = resize_dim
        self.colors = []
        self.bboxes = []
        self.multitracker = cv2.legacy.MultiTracker_create()

    def create_tracker_by_name(self):
        if self.tracker_type == 'BOOSTING':
            return cv2.legacy.TrackerBoosting_create()
        elif self.tracker_type == 'MIL':
            return cv2.legacy.TrackerMIL_create()
        elif self.tracker_type == 'KCF':
            return cv2.legacy.TrackerKCF_create()
        elif self.tracker_type == 'TLD':
            return cv2.legacy.TrackerTLD_create()
        elif self.tracker_type == 'MEDIANFLOW':
            return cv2.legacy.TrackerMedianFlow_create()
        elif self.tracker_type == 'MOSSE':
            return cv2.legacy.TrackerMOSSE_create()
        elif self.tracker_type == 'CSRT':
            return cv2.legacy.TrackerCSRT_create()
        else:
            raise ValueError(f"Invalid tracker type: {self.tracker_type}")

    def select_bounding_boxes(self, frame):
        while True:
            bbox = cv2.selectROI('MultiTracker', frame, fromCenter=False, showCrosshair=True)
            if bbox[2] > 0 and bbox[3] > 0:
                self.bboxes.append(bbox)
                self.colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
            key = cv2.waitKey(0) & 0xFF
            if key == 27:
                break
        cv2.destroyAllWindows()

    def initialize_multitracker(self, frame):
        for bbox in self.bboxes:
            tracker = self.create_tracker_by_name()
            self.multitracker.add(tracker, frame, bbox)

    def track_objects(self):
        video = cv2.VideoCapture(self.video_path)
        if not video.isOpened():
            raise IOError(f"Could not open video: {self.video_path}")

        ok, frame = video.read()
        if not ok:
            raise IOError("Cannot read video file.")

        frame = cv2.resize(frame, self.resize_dim)
        self.select_bounding_boxes(frame)
        self.initialize_multitracker(frame)

        while video.isOpened():
            success, frame = video.read()
            if not success:
                break

            frame = cv2.resize(frame, self.resize_dim)
            success, boxes = self.multitracker.update(frame)
            if not success:
                continue

            for i, newbox in enumerate(boxes):
                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                cv2.rectangle(frame, p1, p2, self.colors[i], 2, 1)

            cv2.imshow('MultiTracker', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        video.release()
        cv2.destroyAllWindows()


"""================================================================"""
"""testing script"""

def main(video_path :str):
    video_path = video_path
    try:
        tracker = MultiObjectTracker(video_path, tracker_type="CSRT")
        tracker.track_objects()
    except Exception as e:
        print(f"Error: {e}")