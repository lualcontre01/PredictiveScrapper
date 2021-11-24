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
    data_lists = []
    if requests.get(URL):
        html_content = requests.get(URL).text
        soup = BeautifulSoup(html_content, "lxml")
        rows = soup.find_all("tr")
        count = len(rows)
        for row in rows:
            print('{}'.format(row.find_all("td")))
            cell = row.find_all("td")
            data_lists.append([row.get_text('//')])
            count = count - 1
        return test_template(data_lists)


@app.route('/test_template/')
def test_template(table):
    return render_template('index.html', table=table)


if __name__ == "__main__":
    app.run(debug=True)
