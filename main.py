from matplotlib.font_manager import FontProperties
import numpy as np
import pandas as pd
import streamlit as st
import requests
import io
from PIL import Image


SUBSCRIPTION_KEY = '582e0c5559ac41c085679445fb960de5'
ep = 'https://20220130tatsuro.cognitiveservices.azure.com/'

assert SUBSCRIPTION_KEY

face_api_url = f'{ep}face/v1.0/detect'

st.title = "title"

uploaded_file = st.file_uploader("Choose an image..", type='jpg')

if uploaded_file is not None:

    img = Image.open(uploaded_file)

    #st.image(img, caption='Uploaded Image.', use_column_width=True)

    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリ取得

#with open('megutatsu.jpg', 'rb') as f:
#with open(uploaded_file.read()) as f:
    #binary_img = f.read()
    
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }

    params = {
            'returnFaceId': 'true',
            'returnFaceAttributes' : 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'

    }

    res = requests.post(face_api_url,params=params,headers=headers,data=binary_img)
    results = res.json()


    #img = Image.open('megutatsu.jpg')
    from PIL import ImageDraw, ImageFont
    fontsize=40
    font = ImageFont.truetype(font="C:\Windows\Fonts\meiryo.ttc",
        size=fontsize)

    draw = ImageDraw.Draw(img)
    for i in range(len(results)):
        result = results[i]
        rect = result["faceRectangle"]
        gender = result["faceAttributes"]["gender"]
        if gender == 'femail':
            gender_jp = '女性'
        else:
            gender_jp = '男性'
        age = result["faceAttributes"]["age"]
        smile = result["faceAttributes"]["smile"]

        draw.text((rect['left'],rect['top']-fontsize-10),f'性別:{gender_jp} 年齢:{age}歳 笑顔:{smile * 100}点',font=font)
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='green',width=5)

        #st.write(result)
    st.write(len(results))
    
    st.image(img)

"""

#my first app

"""