import cv2
from threading import Event, Thread

class TemplateMatcher:
    def __init__(self, video_path, template_path):
        self.video_path = video_path
        self.template_path = template_path
        self.result_available = Event()
        self.stop_order = Event()

    def testFunc(self):
        # This function will run in a separate thread, performing any other tasks concurrently.
        while not self.stop_order.is_set():
            if self.result_available.is_set():
                print("Template found in the frame!")
            else:
                print("Template not found.")

            # Small delay to avoid excessive CPU usage
            self.stop_order.wait(0.5)

    def operation(self):
        # Start the testFunc in a separate thread
        thread1 = Thread(target=self.testFunc)
        thread1.start()

        # Open video and template images
        cap = cv2.VideoCapture(self.video_path)
        searchFor = cv2.imread(self.template_path, cv2.IMREAD_UNCHANGED)

        # Define output video writer with same frame size as the input
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        output_video = cv2.VideoWriter(r'C:\Users\sohel\Downloads\output_with_bounding_boxes.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

        # Open a text file to save bounding box coordinates
        with open("bounding_boxes.txt", "w") as file:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    self.stop_order.set()
                    thread1.join()
                    break

                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                graySearchFor = cv2.cvtColor(searchFor, cv2.COLOR_BGR2GRAY)

                # Template matching
                result = cv2.matchTemplate(grayFrame, graySearchFor, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                print(f"Location: {max_loc}, Confidence: {max_val}")
                
                if max_val > 0.25:
                    print("Found it")
                    self.result_available.set()

                    # Calculate bounding box coordinates
                    top_left = max_loc
                    h, w = graySearchFor.shape
                    bottom_right = (top_left[0] + w, top_left[1] + h)

                    # Write bounding box coordinates to the text file
                    file.write(f"{top_left[0]}, {top_left[1]}, {bottom_right[0]}, {bottom_right[1]}\n")
                    
                    # Draw the bounding box on the frame
                    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                else:
                    self.result_available.clear()

                # Write the frame with bounding box to the output video
                output_video.write(frame)

                if cv2.waitKey(1) == ord('q'):
                    self.stop_order.set()
                    thread1.join()
                    break

        # Release resources
        cap.release()
        output_video.release()
        cv2.destroyAllWindows()

# Usage example:
if __name__ == "__main__":
    video_path = r"C:\Users\sohel\Downloads\Videos_for_project-20241109T110019Z-001\Videos_for_project\street_9.mp4"
    template_path = r'C:\Users\sohel\Downloads\11.jpg'
    matcher = TemplateMatcher(video_path, template_path)
    matcher.operation()
