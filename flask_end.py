from flask import Flask, Response, request
from PIL import Image
import torch
import io
from diffusers import PixArtAlphaPipeline


app = Flask(__name__)



## 初始化模型,第一次调用/image会来执行一次
@app.before_request
def load_model():
    if not hasattr(app, 'pipe'):
        torch.cuda.set_device(0)
        app.pipe = PixArtAlphaPipeline.from_pretrained("PixArt-alpha/PixArt-XL-2-1024-MS", torch_dtype=torch.float16).to("cuda")
        app.pipe.enable_model_cpu_offload()

@app.route('/image', methods=['POST'])
def get_image():
    prompt = request.form.get('prompt')
    
    # 生成图像文件并创建PIL.Image.Image对象
    image = app.pipe(prompt).images[0]

    # 将图像对象转换为字节流
    image_byte_array = image_to_byte_array(image)

    # 返回字节流作为响应，设置mimetype为image/jpeg
    return Response(image_byte_array, mimetype='image/jpeg')

def image_to_byte_array(image):
    byte_array = io.BytesIO()
    image.save(byte_array, format='JPEG')
    byte_array.seek(0)
    return byte_array.getvalue()


if __name__ == '__main__':
    app.run(host='19***', port=7889)
