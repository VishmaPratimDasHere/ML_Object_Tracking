class Dataloader:
  def __init__(self):
    self.Dataloader_v1().draw_data()
  
  class Dataloader_v1:
    def __init__(self):
      self.dtype=None
      self.videos=None

    def draw_data(self):
      # data sampling logic
      self.dtype="Image"

      import os
      import cv2
      video_folders=os.listdir("./ObjectTracking/ObjectTracking/sequences")
      for video_folder in video_folders:
        images=os.listdir(f"./ObjectTracking/ObjectTracking/sequences/{str(video_folder)}")
        height, width, _ = cv2.imread(f"./ObjectTracking/ObjectTracking/sequences/{str(video_folder)}/{images[0]}").shape
        fourcc=cv2.VideoWriter_fourcc(*'mp4v')
        video=cv2.VideoWriter(filename=f"{video_folder}.mp4",fourcc=fourcc, fps=20, frameSize=(width,height))
        for image_name in images:
          image=cv2.imread(f"./ObjectTracking/ObjectTracking/sequences/{str(video_folder)}/{image_name}")
          video.write(image)
        video.release()