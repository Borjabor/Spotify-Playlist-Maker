import requests
from bs4 import BeautifulSoup
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import tkinter as tk
from tkinter import messagebox, ttk
import threading

BILLBOARD_URL = 'https://www.billboard.com/charts/hot-100/'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public'))
user_id = sp.current_user()['id']

def main(year):       
    """
    Opens a TKInter window to ask user for a date, then uses that to retrieve the top 100 songs from Billboard.com. Finally, uses the Spotipy API to create a Spotify playlist with those songs.

	Parameters:
		year (str): The year for which to retrieve the top 100 songs, in YYYY-MM-DD format.

	Returns:
		None
    """

    response = requests.get(BILLBOARD_URL + year)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    top_100_songs = [item.find('h3', id='title-of-a-story').getText().strip() for item in soup.find_all('li', class_='o-chart-results-list__item')  if item.find('h3', id='title-of-a-story') is not None]

    track_uris, not_found_songs = get_track_uris(top_100_songs)
    
    date_object = datetime.strptime(year, "%Y-%m-%d")
    formatted_date = date_object.strftime("%b %Y")
    playlist_name = f"{formatted_date} Billboard 100"
    
    playlist_id = create_playlist(user_id, playlist_name)
    add_tracks_to_playlist(playlist_id, track_uris)
    
    playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"    
    
    show_success_message(playlist_url, not_found_songs)


def show_success_message(playlist_url, not_found_songs):
    def on_success():
        webbrowser.open(playlist_url)
        root.destroy()
        processing_window.destroy()
    
    not_found_message = "\n\nSongs not found in Spotify's library:\n" + "\n".join(not_found_songs) if not_found_songs else ""
    messagebox.showinfo("Success", f"Playlist created successfully!{not_found_message}")
    root.after(100, lambda: on_success())
    
def search_track(track_name):
    search_results = sp.search(q=track_name, type='track', limit=10)
    tracks = search_results['tracks']['items']
    filtered_tracks = [track for track in tracks if track_name.lower() in track['name'].lower()]
    return filtered_tracks

def get_track_uris(track_names):
    uris = []
    not_found_songs = []
    total_tracks = len(track_names)
    for i, track_name in enumerate(track_names):
        try:
            tracks = search_track(track_name)
            if tracks:
                uris.append(tracks[0]['uri'])
            else:
                print(f"No match found for: {track_name}")
                not_found_songs.append(track_name)
        except Exception as e:
            print(f"Error searching for {track_name}: {e}")
            not_found_songs.append(track_name)
        
        progress = int((i + 1) / total_tracks * 100)
        progress_bar['value'] = progress
        processing_window.update_idletasks()
    return uris, not_found_songs

def create_playlist(user_id, playlist_name):
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name)
    return playlist['id']

def add_tracks_to_playlist(playlist_id, track_uris):
    sp.playlist_add_items(playlist_id, track_uris)

def validate_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def on_submit():
    year = entry.get()
    if validate_date(year):
        global processing_window, progress_bar
        processing_window = tk.Toplevel(root)
        processing_window.title("Processing")
        processing_window.geometry("300x100")
        
        label = tk.Label(processing_window, text="Creating playlist, please wait...")
        label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(processing_window, mode='determinate', maximum=100)
        progress_bar.pack(pady=10)
        
        threading.Thread(target=main, args=(year,)).start()
    else:
        messagebox.showerror("Invalid Date", "The date is not in the correct format. Please try again.")
        entry.delete(0, tk.END)
        
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

    
root = tk.Tk()
root.title("Billboard Playlist Creator")

center_window(root, 300, 120)

label = tk.Label(root, text="Enter date to create playlist (YYYY-MM-DD):")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

root.mainloop()