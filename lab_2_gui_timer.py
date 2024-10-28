import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from datetime import datetime, timedelta
import time
import threading
import pygame
from pathlib import Path
import math
import os
import pytz


# Color scheme
COLORS = {
    'primary': '#2d63a7',      # Deep blue
    'secondary': '#4a90e2',    # Light blue
    'accent': '#37c4a3',       # Turquoise
    'warning': '#e74c3c',      # Red
    'background': '#f5f6fa',   # Light gray
    'text': '#2c3e50',         # Dark blue-gray
    'success': '#2ecc71',      # Green
    'header': '#34495e'        # Dark gray-blue
}


class CustomStyle:
    def __init__(self, root):
        self.style = ttk.Style()
        self.root = root
        
        # Configure main window
        self.root.configure(bg=COLORS['background'])
        
        # Configure general styles
        self.style.configure('TFrame', background=COLORS['background'])
        self.style.configure('TLabel', background=COLORS['background'], 
                           foreground=COLORS['text'], font=('Segoe UI', 9))
        self.style.configure('Header.TLabel', font=('Segoe UI', 11, 'bold'), 
                           foreground=COLORS['header'])
        
        # LabelFrame style
        self.style.configure('TLabelframe', background=COLORS['background'], 
                           foreground=COLORS['text'])
        self.style.configure('TLabelframe.Label', font=('Segoe UI', 9, 'bold'), 
                           background=COLORS['background'], foreground=COLORS['primary'])
        
        # Updated Button styles with black text
        self.style.configure('TButton', 
                           font=('Segoe UI', 9, 'bold'),
                           foreground='black',
                           padding=(10, 5))
        
        self.style.map('TButton',
                      foreground=[('pressed', 'black'),
                                ('active', 'black')],
                      background=[('pressed', '!disabled', COLORS['secondary']),
                                ('active', COLORS['secondary'])])
        
        # Primary button style (blue)
        self.style.configure('Primary.TButton',
                           background=COLORS['primary'],
                           foreground='black')
        self.style.map('Primary.TButton',
                      foreground=[('pressed', 'black'),
                                ('active', 'black')],
                      background=[('pressed', '!disabled', COLORS['secondary']),
                                ('active', COLORS['secondary'])])
        
        # Success button style (green)
        self.style.configure('Success.TButton',
                           background=COLORS['success'],
                           foreground='black')
        self.style.map('Success.TButton',
                      foreground=[('pressed', 'black'),
                                ('active', 'black')],
                      background=[('pressed', '!disabled', '#27ae60'),
                                ('active', '#27ae60')])
        
        # Warning button style (red)
        self.style.configure('Warning.TButton',
                           background=COLORS['warning'],
                           foreground='black')
        self.style.map('Warning.TButton',
                      foreground=[('pressed', 'black'),
                                ('active', 'black')],
                      background=[('pressed', '!disabled', '#c0392b'),
                                ('active', '#c0392b')])
        
        # Entry style
        self.style.configure('TEntry', 
                           fieldbackground='white',
                           background='white',
                           foreground=COLORS['text'],
                           padding=5)
        
        # Treeview style
        self.style.configure('Treeview',
                           background='white',
                           foreground=COLORS['text'],
                           rowheight=25,
                           fieldbackground='white')
        self.style.configure('Treeview.Heading',
                           background=COLORS['primary'],
                           foreground='black',
                           font=('Segoe UI', 9, 'bold'))
        self.style.map('Treeview',
                      background=[('selected', COLORS['secondary'])],
                      foreground=[('selected', 'black')])
        
        # Radiobutton style
        self.style.configure('TRadiobutton',
                           background=COLORS['background'],
                           foreground=COLORS['text'],
                           font=('Segoe UI', 9))
        
        # Combobox style
        self.style.configure('TCombobox',
                           background='white',
                           foreground=COLORS['text'],
                           padding=5)
        
        # Additional button hover effects
        self.style.map('TButton',
                      relief=[('pressed', 'sunken'),
                             ('!pressed', 'raised')],
                      bordercolor=[('focus', COLORS['primary'])])


class Timer:
    def __init__(self, name, end_time, timer_type='default', sound_type='beep', action_type='alert', action_path=None):
        self.name = name
        self.end_time = end_time
        self.timer_type = timer_type
        self.sound_type = sound_type
        self.action_type = action_type
        self.action_path = action_path
        self.active = True
        self.thread = None


    def time_remaining(self):
        if not self.active:
            return datetime.timedelta()
        remaining = self.end_time - datetime.now()
        return remaining if remaining.total_seconds() > 0 else datetime.timedelta()


    def is_finished(self):
        return self.time_remaining().total_seconds() <= 0


class TimeZoneManager:
    def __init__(self):
        # Common time zones list 
        self.common_timezones = {
            "Local Time": None,
            "Ukraine (Kyiv)": "Europe/Kiev",
            "UK (London)": "Europe/London",
            "US (New York)": "America/New_York",
            "US (Los Angeles)": "America/Los_Angeles",
            "Japan (Tokyo)": "Asia/Tokyo",
            "Australia (Sydney)": "Australia/Sydney",
            "India (New Delhi)": "Asia/Kolkata",
            "Germany (Berlin)": "Europe/Berlin",
            "China (Beijing)": "Asia/Shanghai"
        }
    

    def get_timezone_names(self):
        return list(self.common_timezones.keys())
    

    def get_current_time(self, timezone_name):
        tz_str = self.common_timezones.get(timezone_name)
        if tz_str is None:  # Local time
            return datetime.now()
        else:
            tz = pytz.timezone(tz_str)
            return datetime.now(pytz.UTC).astimezone(tz)
    

    def convert_to_local(self, dt, from_timezone_name):
        if from_timezone_name == "Local Time" or dt.tzinfo is not None:
            return dt
        
        tz_str = self.common_timezones.get(from_timezone_name)
        if tz_str:
            tz = pytz.timezone(tz_str)
            dt = tz.localize(dt)
            return dt.astimezone(pytz.tzlocal())
        return dt


    def convert_from_local(self, dt, to_timezone_name):
        if to_timezone_name == "Local Time":
            return dt
        
        tz_str = self.common_timezones.get(to_timezone_name)
        if tz_str:
            target_tz = pytz.timezone(tz_str)
            local_tz = pytz.tzlocal()
            
            # If dt is naive, assume it's in local time
            if dt.tzinfo is None:
                dt = local_tz.localize(dt)
            
            return dt.astimezone(target_tz)
        return dt


class AlarmSound:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'beep': self.generate_beep_sound(),
            'melody': self.generate_melody_sound(),
            'gentle': self.generate_gentle_sound()
        }
        self.current_sound = None
        self.playing = False


    def generate_beep_sound(self):
        return self.generate_sound(440.0, 2.0)  # A4 note, 2 beeps per second


    def generate_melody_sound(self):
        return self.generate_sound(523.25, 1.5)  # C5 note, slower beeps


    def generate_gentle_sound(self):
        return self.generate_sound(392.0, 1.0)  # G4 note, gentle beeps


    def generate_sound(self, frequency, beep_freq):
        duration = 3.0
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        buffer = []
        for i in range(samples):
            t = i / sample_rate
            amplitude = math.sin(2 * math.pi * beep_freq * t) * 0.5 + 0.5
            value = 32767 * amplitude * math.sin(2 * math.pi * frequency * t)
            buffer.append(int(value))
        
        import wave
        import struct
        
        filename = f"sound_{frequency}_{beep_freq}.wav"
        with wave.open(filename, "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            for value in buffer:
                data = struct.pack('<h', value)
                wav_file.writeframes(data)
        
        return pygame.mixer.Sound(filename)


    def play(self, sound_type='beep'):
        if self.playing:
            self.stop()
        self.current_sound = self.sounds.get(sound_type, self.sounds['beep'])
        self.current_sound.play(-1)
        self.playing = True


    def stop(self):
        if self.playing and self.current_sound:
            self.current_sound.stop()
            self.playing = False


    def cleanup(self):
        self.stop()
        for filename in os.listdir():
            if filename.startswith("sound_") and filename.endswith(".wav"):
                try:
                    os.remove(filename)
                except:
                    pass


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create a canvas and scrollbar
        self.canvas = tk.Canvas(self, bg=COLORS['background'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create the scrollable frame inside the canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create a window inside the canvas for the scrollable frame
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure canvas to expand horizontally
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Bind mouse wheel to scrolling
        self.bind_mouse_wheel()
        
        # Grid layout for canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


    def on_canvas_configure(self, event):
        # Update the width of the canvas window when the canvas is resized
        self.canvas.itemconfig(self.canvas_frame, width=event.width)


    def bind_mouse_wheel(self):
        # Bind mouse wheel to all relevant widgets
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Bind to canvas
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        

        # Bind to scrollable frame and all its children
        def bind_recursive(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_recursive(child)
        
        bind_recursive(self.scrollable_frame)


class SmartTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Timer")
        self.root.geometry("900x700")
        
        # Apply custom styling
        self.custom_style = CustomStyle(root)
        
        self.alarm = AlarmSound()
        self.timers = []
        
        # Add timezone manager
        self.tz_manager = TimeZoneManager()
        self.current_timezone = tk.StringVar(value="Local Time")
        
        # Timer groups storage remains the same
        self.timer_groups = {
            "Workout": [
                {"name": "Warm-up", "duration": 300, "type": "duration", "sound": "gentle"},
                {"name": "Main Exercise", "duration": 1800, "type": "duration", "sound": "melody"},
                {"name": "Cool-down", "duration": 300, "type": "duration", "sound": "gentle"}
            ],
            "Pomodoro": [
                {"name": "Work Session", "duration": 1500, "type": "duration", "sound": "melody"},
                {"name": "Short Break", "duration": 300, "type": "duration", "sound": "gentle"}
            ],
            "Tea Timer": [
                {"name": "Green Tea", "duration": 180, "type": "duration", "sound": "gentle"},
                {"name": "Black Tea", "duration": 300, "type": "duration", "sound": "beep"}
            ]
        }
        
        # Create main scrollable container
        self.create_scrollable_container()
        
        self.update_timer_list()
        self.update_window_title()
        self.center_window()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def create_scrollable_container(self):
        # Create outer frame that will contain the scroll frame
        outer_frame = ttk.Frame(self.root)
        outer_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights for the root and outer frame
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        outer_frame.grid_rowconfigure(0, weight=1)
        outer_frame.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame
        self.scroll_frame = ScrollableFrame(outer_frame)
        self.scroll_frame.grid(row=0, column=0, sticky="nsew")
        
        # Create widgets inside the scrollable frame
        self.create_widgets()


    def center_window(self):
        """Center the window on the screen and set minimum size"""
        self.root.update_idletasks()
        width = min(900, self.root.winfo_screenwidth() - 100)
        height = min(700, self.root.winfo_screenheight() - 100)
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Set minimum window size
        self.root.minsize(600, 400)


    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.scroll_frame.scrollable_frame, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Application title
        title_label = ttk.Label(main_frame, text="Smart Timer", 
                               font=('Segoe UI', 24, 'bold'), 
                               foreground=COLORS['primary'])
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Timer creation frame with improved spacing
        create_frame = ttk.LabelFrame(main_frame, text="Create New Timer", padding="15")
        create_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        # Timer name with better layout
        name_frame = ttk.Frame(create_frame)
        name_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 10))
        ttk.Label(name_frame, text="Timer Name:", font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, width=40)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        time_format_frame = ttk.LabelFrame(create_frame, text="Time Format", padding="10")
        time_format_frame.grid(row=1, column=0, columnspan=4, pady=(0, 15), padx=5, sticky="ew")
        
        self.timer_type = tk.StringVar(value="duration")
        for i, (text, value) in enumerate([
            ("Duration", "duration"),
            ("Target Time", "target"),
            ("Minutes Only", "minutes"),
            ("Seconds Only", "seconds")
        ]):
            ttk.Radiobutton(time_format_frame, text=text, variable=self.timer_type, 
                           value=value).grid(row=0, column=i, padx=15)

        # Time input with improved layout
        time_frame = ttk.Frame(create_frame)
        time_frame.grid(row=2, column=0, columnspan=4, pady=(0, 15))

        # Variables for different time formats
        self.hours_var = tk.StringVar(value="0")
        self.mins_var = tk.StringVar(value="0")
        self.secs_var = tk.StringVar(value="0")
        self.single_time_var = tk.StringVar(value="0")

        # Standard time inputs with better spacing
        self.standard_time_frame = ttk.Frame(time_frame)
        input_fields = [
            ("Hours:", self.hours_var),
            ("Minutes:", self.mins_var),
            ("Seconds:", self.secs_var)
        ]
        for i, (label_text, var) in enumerate(input_fields):
            ttk.Label(self.standard_time_frame, text=label_text).grid(row=0, column=i*2, padx=(15, 5))
            ttk.Entry(self.standard_time_frame, textvariable=var, width=8).grid(row=0, column=i*2+1, padx=(0, 15))

        # Single value time input
        self.single_time_frame = ttk.Frame(time_frame)
        ttk.Label(self.single_time_frame, text="Time:").grid(row=0, column=0, padx=(0, 10))
        ttk.Entry(self.single_time_frame, textvariable=self.single_time_var, width=15).grid(row=0, column=1)

        self.timer_type.trace('w', self.on_timer_type_change)
        self.on_timer_type_change()

        # Sound type selection with improved layout
        sound_frame = ttk.LabelFrame(create_frame, text="Alert Sound", padding="10")
        sound_frame.grid(row=3, column=0, columnspan=4, pady=(0, 15), padx=5, sticky="ew")

        self.sound_type = tk.StringVar(value="beep")
        for i, (text, value) in enumerate([
            ("Standard Beep", "beep"),
            ("Melody", "melody"),
            ("Gentle", "gentle")
        ]):
            ttk.Radiobutton(sound_frame, text=text, variable=self.sound_type, 
                           value=value).grid(row=0, column=i, padx=15)

        # Time zone selection with improved layout
        timezone_frame = ttk.LabelFrame(create_frame, text="Time Zone", padding="10")
        timezone_frame.grid(row=4, column=0, columnspan=4, pady=(0, 15), padx=5, sticky="ew")
        
        ttk.Label(timezone_frame, text="Select Time Zone:").grid(row=0, column=0, padx=(0, 10))
        self.timezone_combobox = ttk.Combobox(timezone_frame, 
                                             textvariable=self.current_timezone,
                                             values=self.tz_manager.get_timezone_names(),
                                             width=30)
        self.timezone_combobox.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.timezone_time_label = ttk.Label(timezone_frame, text="", style='Header.TLabel')
        self.timezone_time_label.grid(row=0, column=2, padx=15)
        
        self.update_timezone_time()
        
        timezone_frame.columnconfigure(1, weight=1)

        # Create timer button with improved styling
        create_button = ttk.Button(create_frame, text="Create Timer", 
                                 command=self.create_timer, style='Primary.TButton')
        create_button.grid(row=5, column=0, columnspan=4, pady=(5, 0))

        # Timer list frame with improved layout
        list_frame = ttk.LabelFrame(main_frame, text="Active Timers", padding="15")
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=15)

        # Sorting controls with better organization
        sort_frame = ttk.Frame(list_frame)
        sort_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(sort_frame, text="Sort by:", style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 15))
        self.sort_var = tk.StringVar(value="time")
        for text, value in [
            ("Time Remaining", "time"),
            ("Name", "name"),
            ("Type", "type")
        ]:
            ttk.Radiobutton(sort_frame, text=text, variable=self.sort_var, 
                           value=value, command=self.update_timer_list).pack(side=tk.LEFT, padx=10)

        # Next timer info with improved visibility
        self.next_timer_label = ttk.Label(list_frame, text="", style='Header.TLabel')
        self.next_timer_label.grid(row=1, column=0, sticky="w", pady=10)

        # Timer list with improved appearance
        self.tree = ttk.Treeview(list_frame, columns=('Name', 'Remaining', 'Type', 'Sound'), 
                                show='headings', height=8)
        
        # Configure column properties
        columns = {
            'Name': ('Timer Name', 200),
            'Remaining': ('Time Remaining', 150),
            'Type': ('Timer Type', 250),
            'Sound': ('Sound Type', 150)
        }
        
        for col, (heading, width) in columns.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor='center')

        self.tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Add scrollbar with improved integration
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Timer Groups frame with improved layout
        groups_frame = ttk.LabelFrame(main_frame, text="Timer Groups", padding="15")
        groups_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        # Groups controls with better organization
        group_controls = ttk.Frame(groups_frame)
        group_controls.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.groups_list = ttk.Combobox(group_controls, values=list(self.timer_groups.keys()), width=30)
        self.groups_list.pack(side=tk.LEFT, padx=(0, 15))
        
        # Group action buttons with improved styling
        ttk.Button(group_controls, text="Start Group", 
                  command=self.start_timer_group, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(group_controls, text="Save Current as Group", 
                  command=self.save_current_as_group, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(group_controls, text="Delete Group", 
                  command=self.delete_timer_group, 
                  style='Warning.TButton').pack(side=tk.LEFT, padx=5)

        # Preview frame with improved visibility
        self.preview_frame = ttk.Frame(groups_frame)
        self.preview_frame.grid(row=1, column=0, sticky="ew", pady=5)
        
        self.groups_list.bind('<<ComboboxSelected>>', self.update_group_preview)

        # Main control buttons with improved layout and styling
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=15)

        ttk.Button(control_frame, text="Stop Selected", 
                  command=self.stop_selected_timer,
                  style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Remove Completed", 
                  command=self.remove_completed_timers,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop Alarm", 
                  command=self.stop_alarm,
                  style='Warning.TButton').pack(side=tk.LEFT, padx=5)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(2, weight=1)
        groups_frame.columnconfigure(0, weight=1)


    def on_timer_type_change(self, *args):
        # Hide all time input frames
        for widget in self.standard_time_frame.winfo_children():
            widget.grid_remove()
        for widget in self.single_time_frame.winfo_children():
            widget.grid_remove()
        
        # Show appropriate time input based on timer type
        if self.timer_type.get() in ['duration', 'target']:
            self.standard_time_frame.grid()
            for widget in self.standard_time_frame.winfo_children():
                widget.grid()
        else:  # minutes or seconds
            self.single_time_frame.grid()
            for widget in self.single_time_frame.winfo_children():
                widget.grid()


    def update_timezone_time(self):
        """Update the displayed time for the selected timezone"""
        timezone_name = self.current_timezone.get()
        current_time = self.tz_manager.get_current_time(timezone_name)
        self.timezone_time_label.config(
            text=f"Current time: {current_time.strftime('%H:%M:%S')}")
        self.root.after(1000, self.update_timezone_time)  # Update every second


    def create_timer(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a timer name")
            return

        try:
            if self.timer_type.get() in ['duration', 'target']:
                hours = int(self.hours_var.get())
                minutes = int(self.mins_var.get())
                seconds = int(self.secs_var.get())
            else:
                value = int(self.single_time_var.get())
                if self.timer_type.get() == 'minutes':
                    hours = 0
                    minutes = value
                    seconds = 0
                else:  # seconds
                    hours = 0
                    minutes = 0
                    seconds = value
        except ValueError:
            messagebox.showerror("Error", "Please enter valid time values")
            return

        # Get the current timezone
        timezone_name = self.current_timezone.get()
        
        if self.timer_type.get() == "target":
            # Get current time in selected timezone
            current_time = self.tz_manager.get_current_time(timezone_name)
            # Create target time in selected timezone
            end_time = current_time.replace(
                hour=hours, minute=minutes, second=seconds)
            if end_time < current_time:
                end_time += timedelta(days=1)
            # Convert to local time for timer
            end_time = self.tz_manager.convert_to_local(end_time, timezone_name)
        else:
            # For duration-based timers, simply add the duration to current local time
            end_time = datetime.now() + timedelta(
                hours=hours, minutes=minutes, seconds=seconds)

        timer = Timer(name, end_time, self.timer_type.get(), self.sound_type.get())
        timer.thread = threading.Thread(target=self.run_timer, args=(timer,), daemon=True)
        timer.thread.start()
        self.timers.append(timer)

        # Clear inputs
        self.name_var.set("")
        self.hours_var.set("0")
        self.mins_var.set("0")
        self.secs_var.set("0")
        self.single_time_var.set("0")
        
        self.update_window_title()


    def run_timer(self, timer):
        while timer.active and not timer.is_finished():
            time.sleep(0.1)
        
        if timer.active:
            self.alarm.play(timer.sound_type)
            response = messagebox.showinfo(
                "Timer Complete", 
                f"Timer '{timer.name}' has finished!", 
                type=messagebox.OK)
            if response == "ok":
                self.alarm.stop()
            self.update_window_title()


    def update_timer_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get active timers
        active_timers = [t for t in self.timers if t.active and not t.is_finished()]
        
        # Sort timers based on selected criteria
        if self.sort_var.get() == "time":
            active_timers.sort(key=lambda t: t.time_remaining())
        elif self.sort_var.get() == "name":
            active_timers.sort(key=lambda t: t.name.lower())
        else:  # type
            active_timers.sort(key=lambda t: t.timer_type)
        
        # Update next timer info
        if active_timers:
            next_timer = min(active_timers, key=lambda t: t.time_remaining())
            self.next_timer_label.config(
                text=f"Next timer: {next_timer.name} in {str(next_timer.time_remaining()).split('.')[0]}")
        else:
            self.next_timer_label.config(text="No active timers")
        
        # Add current timers to list
        for timer in active_timers:
            remaining = timer.time_remaining()
            current_tz = self.current_timezone.get()
            
            # Convert end time to selected timezone for display
            end_time_tz = self.tz_manager.convert_from_local(
                timer.end_time, current_tz)
            
            self.tree.insert('', 'end', values=(
                timer.name,
                str(remaining).split('.')[0],
                f"{timer.timer_type} (ends: {end_time_tz.strftime('%H:%M:%S')})",
                timer.sound_type
            ))
        
        # Schedule next update
        self.root.after(100, self.update_timer_list)

    def update_window_title(self):
        active_count = len([t for t in self.timers if t.active and not t.is_finished()])
        self.root.title(f"Smart Timer ({active_count} active)")

    def stop_alarm(self):
        self.alarm.stop()

    def stop_selected_timer(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = selected[0]
        timer_name = self.tree.item(item)['values'][0]
        
        for timer in self.timers:
            if timer.name == timer_name:
                timer.active = False
                break
        
        self.update_window_title()

    def remove_completed_timers(self):
        self.timers = [t for t in self.timers if not t.is_finished() and t.active]
        self.update_window_title()

    def update_group_preview(self, event=None):
        # Clear previous preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        selected_group = self.groups_list.get()
        if selected_group in self.timer_groups:
            # Create preview labels
            ttk.Label(self.preview_frame, text="Group contains:", 
                     font=('TkDefaultFont', 9, 'bold')).pack(anchor="w")
            
            for timer_config in self.timer_groups[selected_group]:
                duration_mins = timer_config['duration'] // 60
                duration_secs = timer_config['duration'] % 60
                time_str = f"{duration_mins}m {duration_secs}s" if duration_secs else f"{duration_mins}m"
                
                ttk.Label(self.preview_frame, 
                         text=f"• {timer_config['name']} ({time_str}, {timer_config['sound']} sound)").pack(
                             anchor="w", padx=10)


    def start_timer_group(self):
        selected_group = self.groups_list.get()
        if not selected_group:
            messagebox.showwarning("Warning", "Please select a timer group")
            return
            
        if selected_group not in self.timer_groups:
            messagebox.showerror("Error", "Selected group not found")
            return
            
        # Start all timers in the group
        for timer_config in self.timer_groups[selected_group]:
            end_time = datetime.now() + timedelta(seconds=timer_config['duration'])
            
            timer = Timer(
                timer_config['name'],
                end_time,
                timer_config['type'],
                timer_config['sound']
            )
            timer.thread = threading.Thread(target=self.run_timer, args=(timer,), daemon=True)
            timer.thread.start()
            self.timers.append(timer)
        
        messagebox.showinfo("Success", f"Started all timers in group '{selected_group}'")
        self.update_window_title()


    def save_current_as_group(self):
        # Get active timers
        active_timers = [t for t in self.timers if t.active and not t.is_finished()]
        
        if not active_timers:
            messagebox.showwarning("Warning", "No active timers to save as a group")
            return
            
        # Prompt for group name
        group_name = tk.simpledialog.askstring("Save Timer Group", 
                                             "Enter a name for this timer group:",
                                             parent=self.root)
        
        if not group_name:
            return
            
        # Save timer configurations
        timer_configs = []
        for timer in active_timers:
            remaining = timer.time_remaining()
            duration_seconds = int(remaining.total_seconds())
            
            timer_configs.append({
                "name": timer.name,
                "duration": duration_seconds,
                "type": timer.timer_type,
                "sound": timer.sound_type
            })
        
        self.timer_groups[group_name] = timer_configs
        
        # Update groups list
        self.groups_list['values'] = list(self.timer_groups.keys())
        self.groups_list.set(group_name)
        self.update_group_preview()
        
        messagebox.showinfo("Success", f"Saved current timers as group '{group_name}'")


    def delete_timer_group(self):
        selected_group = self.groups_list.get()
        if not selected_group:
            messagebox.showwarning("Warning", "Please select a timer group to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete the group '{selected_group}'?"):
            del self.timer_groups[selected_group]
            self.groups_list['values'] = list(self.timer_groups.keys())
            self.groups_list.set('')
            self.update_group_preview()
            messagebox.showinfo("Success", f"Deleted timer group '{selected_group}'")


    def on_closing(self):
        self.alarm.cleanup()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = SmartTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    