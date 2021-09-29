
from flask_cors import CORS
from flask import * 
import matplotlib.pyplot as plt 
from skimage.transform import resize
import numpy as np
import nibabel
from matplotlib import cm
import tensorflow
from tensorflow import keras

tensorflow.keras.backend.set_image_data_format('channels_last') 
img_rows = 240
img_cols = 240
smooth = 1.

app = Flask(__name__)  
CORS(app)
model = keras.models.load_model('final_unet_weights.h5', compile=False)
img_rows =240
img_cols =240
def preprocess(imgs):
    imgs_p = np.ndarray((imgs.shape[0], img_rows, img_cols), dtype=np.uint8)
    for i in range(imgs.shape[0]):
        imgs_p[i] = resize(imgs[i], (img_cols, img_rows), preserve_range=True)

    imgs_p = imgs_p[..., np.newaxis]
    return imgs_p

@app.route('/')  
def upload():  
    return render_template("/index.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        img = nibabel.load(  f.filename)
        image_2d = np.reshape(np.array(img.get_fdata()[:, :, 85]),(1,240,240))
        imgs_test = preprocess(image_2d)
        imgs_test = imgs_test.astype('float32')
        imgs_test -= (30.317411)
        imgs_test /= (64.76599)
        plt.imsave('static/new_1.png',imgs_test[0,:,:,0],cmap = cm.bone)
        x = model.predict(imgs_test)
        plt.imsave('static/pred_1.png',x[0,:,:,0],cmap = cm.bone)
        return render_template("/success.html")  
  
if __name__ == '__main__':  
    app.run(host="0.0.0.0")  