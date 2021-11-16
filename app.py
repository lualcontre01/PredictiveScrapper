from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    current_app
)

import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests, validate, json, uuid, pathlib, os

app = Flask(__name__)
URL = 'https://www.ine.gub.uy/indicadores?indicadorCategoryId=42887'


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    if request.method == "POST":
        try:
            global request_url, specific_element, tag
            request_url = request.form.get('urltext')
            tag = request.form.get('SpecificElement')
            source = request.get(request_url).text
            soup = BeautifulSoup(source, "html.parser")
            specific_element = soup.findall(tag)
            counter = len(specific_element)

            image_paths = image_handler(
                tag,
                specific_element,
                request_url
            )

            return render_template("index.html",
                                   url=request_url,
                                   counter=counter,
                                   image_paths=image_paths,
                                   results=specific_element)
        except Exception as e:
            flash(e, "danger")


def image_handler(tag,specific_element,requested_url):
    image_paths = []
    if tag == 'img':
        images = [img['src'] for img in specific_element]
        for i in specific_element:
            image_path = i.atrrs['src']
            valid_imgpath = validate.url(image_path)
            if valid_imgpath == True:
                full_path = image_path
            else:
                full_path = urljoin(requested_url, image_path)
                image_paths.append(full_path)
    return image_paths




if __name__ == "__main__":
    app.run(debug=True)
