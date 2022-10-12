# Video Watermark with Python
# pip install moviepy
from moviepy.editor import *
clip = VideoFileClip("myvideo.mp4", audio=True) 
width,height = clip.size  
text = TextClip("WaterMark", font='Arial', color='white', fontsize=28)
set_color = text.on_color(size=(clip.w + text.w, text.h-10), color=(0,0,0), pos=(6,'center'), col_opacity=0.6)
set_textPos = set_color.set_pos( lambda pos: (max(width/30,int(width-0.5* width* pos)),max(5*height/6,int(100* pos))) )
Output = CompositeVideoClip([clip, set_textPos])
Output.duration = clip.duration
Output.write_videofile("output.mp4", fps=30, codec='libx264')
