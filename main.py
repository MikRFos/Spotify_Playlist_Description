#PLOT IMPORTS
import io
import os

from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

#MY IMPORTS
from database import db
from spotipy import SpotifyException

import spotify_data
import playlist_analysis

#FLASK
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_PATH")
analysis = None
db.init_app(app)

# with app.app_context():
#     db.create_all()

@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/list", methods=["GET", "POST"])
def playlist_analysis_page():
    global analysis
    playlist_url = request.form["playlist"]
    playlist_id = playlist_url.split("/")[-1]
    try:
        playlist = spotify_data.SpotifyPlaylist(playlist_id)
    except TypeError:
        print("Playlist not found")
        return render_template("index.html")
    else:
        try:
            songs = playlist.get_songs()
        except SpotifyException:
            print("Error")
            return render_template("index.html")
        else:
            analysis = playlist_analysis.PlaylistAnalysis(songs)
            print(analysis.playlist_df)
            data = {
                "key_mode": analysis.get_common("key"),
                "signature_mode": analysis.get_common("signature"),
                "average_tempo": analysis.get_average("tempo"),
            }
            return render_template("playlist.html", songs=songs, data=data)


@app.route('/plot.png')
def plot_png():
    fig = analysis.plot_data("key")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)
