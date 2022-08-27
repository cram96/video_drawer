import cv2
from base64 import encode
from urllib import response
import gradio as gr
import requests
from PIL import Image
import os
import app
def video_splitter(path_to_video,saving_folder):

    """this function splits a video into frames
        path_to_video: path where the original video is allocated
        saving_folder: path where frames will be saved   
    """

    vidcap = cv2.VideoCapture(path_to_video)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(saving_folder+"/"+"%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1

def frame_converter(frame_to_convert,path_with_saved_frames,saving_folder):
    """
        legacy code, uses api call in stead of local model
        data = gr.processing_utils.encode_url_or_file_to_base64(path_with_saved_frames+frame_to_convert)

        r = requests.post(url='https://hf.space/embed/carolineec/informativedrawings/+/api/predict/', json={"data": [data,"style 1"]})
        my_json = r.json().get('data')[0]
        img = gr.processing_utils.decode_base64_to_file(my_json, encryption_key=None, file_path=None)

        import tempfile, shutil
        
        f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        
        f.write('foo')
        
        file_name = img.name
        
        f.close()
        
        shutil.copy(file_name, saving_folder+"/"+frame_to_convert)

    """   
    img = app.predict(path_with_saved_frames+frame_to_convert,"style 2")
    img.save(saving_folder+frame_to_convert)

def video_maker(path_of_frames,name_of_video):

    import numpy as np
    import glob
    import os
    img_array = []

    file_list = os.listdir(path_of_frames) 
    file_list = [x.replace(".jpg","") for x in file_list]
    file_list.sort(key=int)
    file_list = [path_of_frames+x+".jpg" for x in file_list]
    
    for filename in file_list:
        print(filename)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)


    out = cv2.VideoWriter(name_of_video,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, size)
 
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()



def main(path_to_original_video=None,
        path_to_save_frames=None,
        path_to_save_drawed_frames=None,
        name_of_video=None):

    if None in locals().values():
        if not os.path.exists("frames"):
            os.mkdir("frames")
        if not os.path.exists("converted"):
            os.mkdir("converted")   
        path_to_original_video = 'test.mp4'
        path_to_save_frames = "frames/"
        path_to_save_drawed_frames="converted/"
        name_of_video='test_drawed.mp4'
   
    
    video_splitter(path_to_original_video,path_to_save_frames)


    for file in os.listdir(path_to_save_frames):
        frame_converter(file,path_to_save_frames,path_to_save_drawed_frames)
    
    video_maker(path_to_save_drawed_frames,name_of_video)




main()

