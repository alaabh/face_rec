import os

import shutil


def decoupage(nom_video):
  
    pos2 = nom_video.find('.mp4')
    nom = nom_video[0:pos2]
    print (nom)
    print (nom_video)
    os.mkdir('picture/'+nom)
    os.system("ffmpeg -i video/"+nom_video+" -r 1 -f image2 picture/"+nom+"/output%d.jpg")
    shutil.copy('video/'+nom_video, 'picture/'+nom)
    os.remove('video/'+nom_video)

