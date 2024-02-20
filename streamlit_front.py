import streamlit as st
from PIL import Image
import io
import pandas as pd
import numpy as np
import requests

def get_image(prompt):
    
    # 发起 POST 请求并传递提示信息
    response = requests.post('http://19***4:7889/image', data={'prompt': prompt})
    
    # 获取图像字节流
    image_bytes = response.content
    
    # 将字节流转换为图像对象
    image = Image.open(io.BytesIO(image_bytes))

    return image


# 初始化变量
if 'image1' not in st.session_state:
    st.session_state.image1 = None

 

if __name__ == '__main__':
    st.title('AI文生图')

    # 创建文本输入框
    prompt = st.text_input('请输入提示词，暂时只支持英文prompt')
    
    # 监听按钮点击事件
    if st.button("生成图像"):
        with st.spinner("正在生成图像..."):
            # 生成图像
            st.session_state.image1 = get_image(prompt)
        # 显示图像
        st.image(st.session_state.image1)
