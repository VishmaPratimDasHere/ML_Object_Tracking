class Dataloader:

  class Dataloader_v1:
    def draw_data(self,_fps=25):
      # data sampling logic
      import os
      import cv2
      video_folders=os.listdir("./ObjectTracking/ObjectTracking/sequences")
      for video_folder in video_folders:
        images=os.listdir(f"./ObjectTracking/ObjectTracking/sequences/{str(video_folder)}")
        height, width, _ = cv2.imread(f"./ObjectTracking/ObjectTracking/sequences/{str(video_folder)}/{images[0]}").shape
        fourcc=cv2.VideoWriter_fourcc(*'mp4v')
        os.makedirs(f"./{_fps}", exist_ok=True)
        video=cv2.VideoWriter(filename=f"./{_fps}/{video_folder}.mp4",fourcc=fourcc, fps=_fps, frameSize=(width,height))
        for image_name in images:
          image=cv2.imread(f"./ObjectTracking/ObjectTracking/sequences/{str(video_folder)}/{image_name}")
          video.write(image)
        video.release()

  def __init__(self):
    self.dataloader=self.Dataloader_v1()

  def load_data(self, _fps=25):
    self.dataloader.draw_data(_fps=_fps)


