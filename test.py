import gradio as gr
from app import predict
img = predict("frames/0.jpg","style 2")
print(dir(img))
img.save("0_2.jpg")