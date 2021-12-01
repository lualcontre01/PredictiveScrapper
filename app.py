import pandas as pd
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
        table1 = soup.find('table')
        headers = []
        for i in table1.find_all('th'):
            tittle = i.text
            data_lists.append(tittle)
        my_data = pd.DataFrame(columns=data_lists)
        for j in table1.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(my_data)
            my_data.loc[length] = row
        return test_template(my_data)


@app.route('/test_template/')
def test_template(table):
    return render_template('index.html', table=table)


if __name__ == "__main__":
    app.run(debug=True)
