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
    response = requests.get(URL)
    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        table1 = soup.find('table')
        columns = [title.text for title in table1.find_all('th')]
        my_data = pd.DataFrame(columns=columns)
        index_values = []
        for j in table1.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            for i in row_data:
                index_values.append(i.text)
                print('index {}'.format(index_values))
            print('Ros {}'.format(row))
            length = len(my_data)
            my_data.loc[length] = row
        return test_template(my_data)


@app.route('/test_template/')
def test_template(table):
    return render_template('index.html', table=table)


if __name__ == "__main__":
    app.run(debug=True)
