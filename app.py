import os
from flask import Flask, render_template, request, helpers, send_file
import cv2

app = Flask(__name__, static_folder='./build/static',
            template_folder='./build')


def mosaic(img, rect, size):
    # detect area to layer mosaic
    (x1, y1, x2, y2) = rect
    w = x2 - x1
    h = y2 - y1
    i_rect = img[y1:y2, x1:x2]

    # shrink img => expand img
    i_small = cv2.resize(i_rect, (size, size))
    i_mos = cv2.resize(i_small, (w, h), interpolation=cv2.INTER_AREA)

    # layer mosaic on original
    img2 = img.copy()
    img2[y1:y2, x1:x2] = i_mos
    return img2


def mosaicImage():
    cascade_file = 'haarcascade_frontalface_alt.xml'
    cascade = cv2.CascadeClassifier(cascade_file)

    img = cv2.imread('./images/tmp.jpg')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_list = cascade.detectMultiScale(img_gray, minSize=(150, 150))
    if len(face_list) == 0:
        quit()

    for (x, y, w, h) in face_list:
        img = mosaic(img, (x, y, x+w, y+h), 10)

    cv2.imwrite('./images/tmp.jpg', img)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/upload", methods=['POST'])
def upload():
    print('request reached')
    if not request.files:
        print('no image selected')
        return 'no image selected'
    img_file = request.files['myFile']
    filename = img_file.filename
    img_file.save('./images/tmp.jpg')
    mosaicImage()
    return send_file('./images/tmp.jpg')

    response = helpers.make_response('dummy response')
    return response
    print('we sent image!')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8888)

