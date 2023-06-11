from flask import Flask, render_template, request, redirect, url_for, flash
import json, os, webbrowser
from pytube import YouTube

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gfkefozhjuOHUNobobOB4588uo'

#region Global variables
url = str
video = YouTube
#endregion

#region Getters Setters
def get_path():
    with open('settings.json') as file:
        data = json.load(file)
    return str(data['path'])

def get_rescuePath():
    with open('settings.json') as file:
        data = json.load(file)
    return str(data['rescuePath'])

def set_settings(content):
    with open('settings.json', 'w') as file:
        json.dump(content, file, indent=2)
#endregion

#region Methods
def downloadMusic(path: str, file_name: str):
    audio = video.streams.filter(only_audio=True).first()
    out_file = audio.download(output_path = path, filename = file_name)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    return os.rename(out_file, new_file)
#endregion

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        global url
        url = request.form['url']
        return redirect(url_for('download'))
        
    return render_template('index.html')

@app.route('/downloading', methods=('GET', 'POST'))
def download():
    global video
    video = YouTube(url)
    if request.method == 'POST':
        file_name = request.form['title']
        if os.path.exists(get_path()):
            downloadMusic(get_path(), file_name)
        elif os.path.exists(get_rescuePath()):
            downloadMusic(get_rescuePath(), file_name)
        else:
            flash('Problème de paramétrage !','error')
            return redirect(url_for('index'))
               
        flash('Chanson sauvegardée !','message')
        return redirect(url_for('index'))
    
    videoID = (url.split("="))[1].split("&")
    try:
        new_title = video.title.replace("|","-")
        return render_template('downloading.html', video = new_title, videoID = videoID[0])
    except:
        flash('Problème de téléchargement de la musique ! Veuillez réessayer !','error')
        return redirect(url_for('index'))

@app.route('/settings', methods=('GET', 'POST'))
def settings():
    if request.method == 'POST':
        path = request.form['path']
        rescuePath = request.form['rescuePath']
        json_obj = json.loads('{"path":"' + path + '", "rescuePath": "' + rescuePath + '"}')
        set_settings(json_obj)
        flash('Paramétrage sauvegardé !','message')
        return redirect(url_for('index'))
    
    return render_template('settings.html', path = get_path(), rescuePath = get_rescuePath())

if __name__ == "__main__":
    # webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)