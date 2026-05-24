# Import necessary libraries
import os
import tkinter as tk 
from PIL import Image, ImageTk # Used for loading PNG/JPG icons
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume # For controlling system audio


# Main application class
class VolumeMixerApp:
    # The constructor method, called when a new VolumeMixerApp object is created
    def __init__(self, root_window):
        self.root_window = root_window # Store the main window
        self.root_window.title("Mini Volume Mixer")
        self.root_window.geometry("400x600")
        self.root_window.minsize(350, 200) # Set a reasonable minimum size

        # --- Set Window Icon ---
        try:
            # Try to load icon from multiple possible locations
            icon_paths = [
                "AMRAAM-Chan hum.png",  # Same directory as script
                "AMRAAM-Chan hum.ico",  # Same directory as script (if converted to ICO)
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "AMRAAM-Chan hum.png"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "AMRAAM-Chan hum.ico"),
                os.path.join(os.path.expanduser("~"), "Documents", "Forbidden content", "AMRAAM-Chan hum.png"),
                os.path.join(os.path.expanduser("~"), "Documents", "Forbidden content", "AMRAAM-Chan hum.ico"),
            ]
            
            self.icon_image = None
            for path in icon_paths:
                try:
                    if path.lower().endswith('.ico'):
                        # For ICO files
                        self.root_window.iconbitmap(path)
                        print(f"Loaded icon from: {path}")
                        break
                    else:
                        # For PNG files
                        img = Image.open(path)
                        self.icon_image = ImageTk.PhotoImage(img)
                        self.root_window.iconphoto(False, self.icon_image)
                        print(f"Loaded icon from: {path}")
                        break
                except Exception as e:
                    continue
            else:
                print("Warning: Could not load application icon. Using default icon.")
        except Exception as e:
            print(f"Warning: Could not load icon. Is 'Pillow' installed? Error: {e}")

        self.root_window.resizable(True, True)
        self.root_window.configure(bg="#0d6666")

        # Initialize lists and dictionaries to hold audio session data and GUI widgets
        self.sessions = []
        self.slider_vars = {}
        self.slider_widgets = {}
        self.mute_buttons = {}
        self.volume_labels = {}

        # --- Create a scrollable area for the volume sliders ---
        # A Canvas widget is used to create a scrollable region
        canvas = tk.Canvas(self.root_window)
        # A Scrollbar widget that is linked to the canvas's y-view
        scrollbar = tk.Scrollbar(self.root_window, orient="vertical", command=canvas.yview)
        # A Frame widget placed inside the canvas, which will contain the actual content (labels and sliders)
        self.scroll_frame = tk.Frame(canvas)

        # When the scroll_frame's size changes, update the canvas's scrollable region
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Add the scroll_frame to the canvas
        self.scroll_window = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a "Refresh" button and pack it to the bottom of the window
        # The configuration options (bg, fg) are passed directly to the constructor.
        # The .pack() method is called on the widget itself, but since it returns None,
        # we cannot chain any more methods after it.
        tk.Button(
            self.root_window, text="Refresh", command=self.refresh_sessions,
            bg="#004c4c", fg="white", activebackground="#006666", activeforeground="white",
            relief="flat", borderwidth=0
        ).pack(side="bottom", fill="x", pady=5, padx=5)

        # Pack the canvas and scrollbar into the main window
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Initial call to populate the mixer with current audio sessions
        self.refresh_sessions()

    # Method to find and display all current audio sessions
    def refresh_sessions(self):
        # Destroy all existing widgets in the scroll_frame to prevent duplicates
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Get all active audio sessions from the system using pycaw
        self.sessions = AudioUtilities.GetAllSessions()
        # Clear the dictionaries that store slider data
        self.slider_vars.clear()
        self.slider_widgets.clear()
        self.mute_buttons.clear()
        self.volume_labels.clear()

        for i, session in enumerate(self.sessions):
            if session.Process:
                # If multiple sessions exist for one app, we need a unique name for keys.
                # We'll use the process name for display, but a unique key for our dictionaries.
                display_name = session.Process.name()
                unique_key = f"{display_name}_{i}"

                # Use 2 rows per application to make space for the volume label
                base_row = i * 2

                # Create a label to display the application's name
                label = tk.Label(self.scroll_frame, text=display_name, anchor="w")
                label.grid(row=base_row, column=0, sticky="w", rowspan=2)

                # --- Volume Slider ---
                slider_var = tk.DoubleVar()
                # Get the audio control interface for the session
                volume = session._ctl.QueryInterface(ISimpleAudioVolume).GetMasterVolume()
                # Set the slider's variable to the current volume, scaled to 0-100
                slider_var.set(volume * 100)

                # Create the volume slider widget
                slider = tk.Scale(
                    self.scroll_frame, from_=0, to=100, orient="horizontal",
                    variable=slider_var, length=200,
                    showvalue = False,
                    
                    # Pass the unique key to the callback
                    command=lambda val, s=session, key=unique_key: self._update_volume_and_label(s, key, val)
                )
                slider.grid(row=base_row, column=1, pady=(0, 10))

                # --- Volume Value Label ---
                # Create a label to show the numeric value of the volume
                volume_label = tk.Label(self.scroll_frame, text=f"{int(slider_var.get())}%")
                volume_label.grid(row=base_row + 1, column=1)

                # Store the slider variable and widget for future reference
                self.slider_vars[unique_key] = slider_var
                self.slider_widgets[unique_key] = slider
                self.volume_labels[unique_key] = volume_label

                # --- Mute Button ---
                # Get the mute status (0=Unmuted, 1=Muted)
                is_muted = session._ctl.QueryInterface(ISimpleAudioVolume).GetMute()
                mute_text = "Unmute" if is_muted else "Mute"

                # Create the mute/unmute button
                mute_button = tk.Button(
                    self.scroll_frame, text=mute_text,
                    # The command calls toggle_mute, passing the session and its unique key
                    command=lambda s=session, key=unique_key: self.toggle_mute(s, key)
                )
                mute_button.grid(row=base_row, column=2, padx=5, rowspan=2)

                self.mute_buttons[unique_key] = mute_button

    def _update_volume_and_label(self, session, unique_key, value_str):
        """A helper that sets volume and updates the corresponding value label."""
        # Set the system volume for the application
        self.set_volume(session, value_str)
        # Update the text of the volume label
        self.volume_labels[unique_key].config(text=f"{int(float(value_str))}%")

    def toggle_mute(self, session, unique_key):
        """Toggles the mute state for a given audio session."""
        try:
            volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
            # Get current mute state (0 for not muted, 1 for muted)
            current_mute_state = volume_interface.GetMute()
            # Set the new state to the opposite of the current one
            new_mute_state = not current_mute_state
            volume_interface.SetMute(new_mute_state, None)

            # Update the button's text to reflect the new state
            button = self.mute_buttons[unique_key]
            button.config(text="Unmute" if new_mute_state else "Mute")
        except Exception as e:
            print(f"Error toggling mute for session {unique_key}: {e}")

    # Method to set the volume for a specific audio session
    def set_volume(self, session, value):
        try:
            # Get the volume control interface for the session
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            # Set the master volume. The value from the slider (0-100) is converted back to 0.0-1.0
            volume.SetMasterVolume(float(value) / 100.0, None)
        except Exception as e:
            print("Error setting volume:", e)

# This block runs only when the script is executed directly
if __name__ == "__main__":
    root = tk.Tk() # Create the main tkinter window
    app = VolumeMixerApp(root) # Create an instance of our application class
    root.mainloop() # Start the tkinter event loop to run the GUI
