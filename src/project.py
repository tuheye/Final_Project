import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar, messagebox
from tkinter import ttk
from spotipy.exceptions import SpotifyException

# Spotify credentials
CLIENT_ID = "e0d5b1c2d4e541b380d4db3fbce1ddbc"
CLIENT_SECRET = "2d485d5aef79438f9515742f871e3039"
REDIRECT_URI = "https://open.spotify.com/user/k8498hv6sm44709mnhnu07hug"
SCOPE = "playlist-modify-public playlist-read-private"

# Initialize Spotify client
spotify_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                             client_secret=CLIENT_SECRET,
                             redirect_uri=REDIRECT_URI,
                             scope=SCOPE)
sp = spotipy.Spotify(auth_manager=spotify_oauth)


def search_tracks_by_mood(mood, limit):
    """Search for tracks matching the given mood."""
    try:
        query = f"track:{mood}"  # Use mood as a query
        results = sp.search(q=query, type='track', limit=limit)
        tracks = results.get('tracks', {}).get('items', [])
        track_ids = [track['id'] for track in tracks]
        return track_ids
    except SpotifyException as e:
        messagebox.showerror("Error", f"Spotify API error: {e}")
        return []


def create_playlist(user_id, playlist_name, mood):
    """Create a playlist in the user's Spotify account with a custom name."""
    try:
        description = f"A playlist for {mood} vibes."
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=description)
        return playlist['id']
    except SpotifyException as e:
        messagebox.showerror("Error", f"Could not create playlist: {e}")
        return None


def add_tracks_to_playlist(playlist_id, track_ids):
    """Add tracks to the playlist."""
    try:
        sp.playlist_add_items(playlist_id=playlist_id, items=track_ids)
    except SpotifyException as e:
        messagebox.showerror("Error", f"Could not add tracks to playlist: {e}")


def generate_playlist():
    """Handle the playlist generation process."""
    mood = mood_var.get().strip().lower()
    playlist_name = name_var.get().strip()
    num_songs = num_songs_var.get()

    if not mood:
        messagebox.showerror("Error", "Please enter a mood.")
        return
    if not playlist_name:
        messagebox.showerror("Error", "Please enter a playlist name.")
        return
    if num_songs <= 0:
        messagebox.showerror("Error", "Number of songs must be greater than 0.")
        return

    try:
        user_id = sp.me()['id']
        messagebox.showinfo("Processing", f"Searching for {num_songs} tracks matching the mood: {mood}...")
        track_ids = search_tracks_by_mood(mood, limit=num_songs)

        if not track_ids:
            messagebox.showerror("Error", f"No tracks found for mood: {mood}. Try another mood.")
            return

        messagebox.showinfo("Processing", f"Creating playlist: {playlist_name}...")
        playlist_id = create_playlist(user_id, playlist_name, mood)

        if not playlist_id:
            return

        messagebox.showinfo("Processing", "Adding tracks to playlist...")
        add_tracks_to_playlist(playlist_id, track_ids)

        messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully! Check your Spotify account.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


# GUI Application
def create_app():
    app = Tk()
    app.title("Spotify Mood Playlist Creator")
    app.geometry("500x400")
    app.configure(bg="#282C34")

    # Title Banner
    Label(app, text="Spotify Mood Playlist Creator", bg="#61AFEF", fg="white",
          font=("Helvetica", 18, "bold"), pady=10).pack(fill="x")

    # Input Frame
    input_frame = ttk.Frame(app, padding="20 10")
    input_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Mood input
    ttk.Label(input_frame, text="Enter a Mood:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
    global mood_var
    mood_var = StringVar()
    ttk.Entry(input_frame, textvariable=mood_var, width=30).grid(row=0, column=1, pady=5)

    # Playlist name input
    ttk.Label(input_frame, text="Playlist Name:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
    global name_var
    name_var = StringVar()
    ttk.Entry(input_frame, textvariable=name_var, width=30).grid(row=1, column=1, pady=5)

    # Number of songs input
    ttk.Label(input_frame, text="Number of Songs:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
    global num_songs_var
    num_songs_var = IntVar(value=20)  # Default to 20 songs
    ttk.Entry(input_frame, textvariable=num_songs_var, width=10).grid(row=2, column=1, pady=5, sticky="w")

    # Create Playlist Button
    ttk.Button(app, text="Create Playlist", command=generate_playlist).pack(pady=20)

    # Footer
    Label(app, text="Powered by Spotify", bg="#282C34", fg="white", font=("Arial", 10)).pack(side="bottom", pady=10)

    app.mainloop()


if __name__ == "__main__":
    create_app()
