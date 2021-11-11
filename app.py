from flask import Flask
import requests
import lxml.html as lh
import pandas as pd

app = Flask(__name__)
URL = 'https://www.ine.gub.uy/indicadores?indicadorCategoryId=42887'


@app.route("/")
def get_data():
    page = requests.get(URL)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    col = []
    i = 0
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        print('%d:"%s"' % (i, name))
        col.append((name, []))

    for j in range(1, len(tr_elements)):
        # T is our j'th row
        T = tr_elements[j]
        # If row is not of size 10, the //tr data is not from our table
        if len(T) != 10:
            break
        # i is the index of our column
        i = 0
        # Iterate through each element of the row
        for t in T.iterchildren():
            data = t.text_content()
            # Check if row is empty
            if i > 0:
                # Convert any numerical value to integers
                try:
                    data = int(data)
                except:
                    pass
            # Append the data to the empty list of the i'th column
            col[i][1].append(data)
            # Increment i for the next column
            i += 1
    return pd.DataFrame({title: column for (title, column) in col}).head()
