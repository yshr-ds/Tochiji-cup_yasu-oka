from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def root():
    markers=[
    {
    'lat':35.68066659206367,
    'lon':139.7681614127473,
    'popup':'This is sample website of the Tochiji cup.'
        }
    ]
    return render_template('index.html',markers=markers )

if __name__ == "__main__":
    app.run(debug = True)
