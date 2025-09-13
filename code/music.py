import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
import os

class MusicPlayer:

    def __init__(self, root):
        self.root = root
        self.root.title("Music Player:A Feature-Rich Multimedia Experience")
        self.root.geometry("800x400")
        self.root.resizable(False, False)

        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        # Variables
        self.playlist = []
        self.current_index = 0
        self.paused = False

        # Load Background Image
        bg_image_path = os.path.join(os.getcwd(), "musicplayerbackground.png")
        self.bg_image = tk.PhotoImage(file=bg_image_path)
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Initialize Canvases for Animation
        self.canvas1 = tk.Canvas(self.root, width=20, height=300, bg='white')
        self.canvas1.place(x=30, y=50)

        self.canvas = tk.Canvas(self.root, width=20, height=300, bg='white')
        self.canvas.place(x=750, y=50)

        # GUI Elements
        self.create_widgets()

        # Song Progress Update
        self.song_progress_update()

    def create_widgets(self):
        # Playlist Listbox
        self.playlist_listbox = tk.Listbox(self.root, width=50, height=5, font=("Arial", 12), bg="lavender")
        self.playlist_listbox.place(x=170, y=50)
        self.playlist_listbox.bind("<Double-1>", self.on_double_click)

        # Buttons Frame
        self.buttons_frame = ttk.Frame(self.root, width=400, height=-10, style="ghostwhite.TFrame")
        self.buttons_frame.place(x=100, y=170)

        # Play/Pause Button
        self.play_pause_button = ttk.Button(self.buttons_frame, text="Play", command=self.play_pause)
        self.play_pause_button.grid(row=0, column=0, padx=10, pady=5)

        # Stop Button
        self.stop_button = ttk.Button(self.buttons_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=1, padx=10, pady=5)

        # Previous Button
        self.previous_button = ttk.Button(self.buttons_frame, text="Previous", command=self.previous)
        self.previous_button.grid(row=0, column=2, padx=10, pady=5)

        # Next Button
        self.next_button = ttk.Button(self.buttons_frame, text="Next", command=self.next)
        self.next_button.grid(row=0, column=3, padx=10, pady=5)

        # Volume Label
        self.volume_label = ttk.Label(self.buttons_frame, text="Volume:")
        self.volume_label.place(x=250, y=45)

        # Volume Scale
        self.volume_var = tk.DoubleVar()
        self.volume_scale = ttk.Scale(self.buttons_frame, from_=0, to=1, orient="horizontal", variable=self.volume_var, command=self.set_volume)
        self.volume_scale.set(0.5)  # initial volume
        self.volume_scale.grid(row=1, column=1, columnspan=3, padx=10, pady=5)

        # Import Button
        self.import_button = ttk.Button(self.buttons_frame, text="Import Music", command=self.import_music)
        self.import_button.grid(row=2, column=0, columnspan=4, pady=5)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.buttons_frame, orient="horizontal", length=600, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=4, pady=5)
        self.progress_bar.bind("<Button-1>", self.seek_to_position)  # Bind left-click to seek

        # Status Label
        self.status_label = ttk.Label(self.buttons_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=4, column=0, columnspan=4, pady=10)

        # Style configuration for the buttons frame
        style = ttk.Style()
        style.configure("ghostwhite.TFrame", background="ghostwhite")

    def import_music(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3;*.wav")])
        for file_path in file_paths:
            if file_path not in self.playlist:
                self.playlist.append(file_path)
                self.playlist_listbox.insert(tk.END, os.path.basename(file_path))

    def play_pause(self):
        if not self.playlist:
            messagebox.showinfo("Info", "Playlist is empty. Import some music.")
            return

        if pygame.mixer.music.get_busy() and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            self.play_pause_button.config(text="Play")
        else:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.play_pause_button.config(text="Pause")
            else:
                self.play_music()
                self.animate_music()  # Start animation when music plays
    def play_music(self):
        if not self.playlist:
            messagebox.showinfo("Info", "Playlist is empty. Import some music.")
            return

        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play()
        self.paused = False
        self.play_pause_button.config(text="Pause")
        self.status_label.config(text=f"Now Playing: {os.path.basename(self.playlist[self.current_index])}")

    def stop(self):
        pygame.mixer.music.stop()
        self.paused = False
        self.play_pause_button.config(text="Play")
        self.progress_bar.stop()

    def previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.play_music()
        else:
            messagebox.showinfo("Info", "This is the first song in the playlist.")

    def next(self):
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.play_music()
        else:
            messagebox.showinfo("Info", "This is the last song in the playlist.")

    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

    def song_progress_update(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            current_time = pygame.mixer.music.get_pos() / 1000  # in seconds
            song_length = pygame.mixer.Sound(self.playlist[self.current_index]).get_length()  # in seconds
            progress_percentage = (current_time / song_length) * 100
            self.progress_bar["value"] = progress_percentage
            minutes, seconds = divmod(int(current_time), 60)
            self.status_label.config(text=f"Now Playing: {os.path.basename(self.playlist[self.current_index])} - {minutes:02}:{seconds:02}")
        else:
            self.progress_bar["value"] = 0

        self.root.after(1000, self.song_progress_update)

    def animate_music(self):
        # Example animation: move a rectangle up and down on both canvases
        self.canvas1.delete("all")  # Clear previous animation
        self.canvas.delete("all")   # Clear previous animation
        x1, y1 = 0, 10
        x2, y2 = 50, 50
        direction1, direction2 = 1, 1  # Direction for both canvases
        while pygame.mixer.music.get_busy() and not self.paused:
            # Animation on the first canvas
            self.canvas1.create_rectangle(x1, y1, x2, y2, fill="lightsalmon")
            y1 += 5 * direction1
            y2 += 5 * direction1
            if y2 >= 300 or y1<= 0:  # Reverse direction at canvas boundaries
                direction1 *= -1

            # Animation on the second canvas
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightsalmon")
            y1 += 5 * direction2
            y2 += 5 * direction2
            if y2 >= 300 or y1 <= 0:  # Reverse direction at canvas boundaries
                direction2 *= -1

            self.canvas1.update()
            self.canvas.update()
            self.root.after(30)  # Adjust speed of animation

    def seek_to_position(self, event):
        if pygame.mixer.music.get_busy() and not self.paused:
            x = event.x
            song_length = pygame.mixer.Sound(self.playlist[self.current_index]).get_length()  # in seconds
            total_pixels = self.progress_bar.winfo_width()
            percentage = (x / total_pixels) * 100
            pygame.mixer.music.set_pos(percentage * song_length / 100)

    def on_double_click(self, event):
        selected_index = self.playlist_listbox.curselection()
        if selected_index:
            self.current_index = selected_index[0]
            self.play_music()
            self.animate_music()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
