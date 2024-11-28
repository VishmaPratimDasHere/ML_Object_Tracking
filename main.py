from ML_Object_Tracking.dataloader.Dataloader import Dataloader
from ML_Object_Tracking.model import model

video_path=None

if input("Do you have your own test video? (Enter y/n)")=="n":
    for _fps in range(26,31):
        data = Dataloader()
        data.load_data(_fps=_fps)
    video_path = input("\nVideos have been generated and foldered by fps. \nPlease enter video path :")

else:
    video_path = input("\nPlease enter video path :")

model.main(video_path)

