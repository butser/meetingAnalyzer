"""
Graphical User Interface for Meeting Analyzer
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from .analyzer import MeetingAnalyzer
from .profiles import list_profiles, get_profile_description


class MeetingAnalyzerGUI:
    """Main GUI application for Meeting Analyzer"""
    
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("Meeting Analyzer - Local AI Analysis")
        self.root.geometry("900x800")
        
        # Set minimum size
        self.root.minsize(800, 600)
        
        # Analysis state
        self.analyzer = None
        self.analysis_thread = None
        self.stop_requested = False
        self.results = {}
        
        # Message queue for thread communication
        self.message_queue = queue.Queue()
        
        # Load environment variables
        load_dotenv()
        
        # Setup UI
        self.setup_ui()
        
        # Load saved settings
        self.load_settings()
        
        # Start queue processor
        self.process_queue()
    
    def setup_ui(self):
        """Create all GUI elements"""
        # Create main container with scrollbar
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Meeting Analyzer - Local AI Analysis",
            font=("TkDefaultFont", 16, "bold")
        )
        title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Create sections
        row = 1
        row = self.create_input_section(main_frame, row)
        row = self.create_project_section(main_frame, row)
        row = self.create_frame_extraction_section(main_frame, row)
        row = self.create_progress_section(main_frame, row)
        row = self.create_control_buttons(main_frame, row)
        row = self.create_results_section(main_frame, row)
        
        # Configure grid row weights
        for i in range(row):
            main_frame.rowconfigure(i, weight=0)
        main_frame.rowconfigure(4, weight=1)  # Progress section should expand
    
    def create_input_section(self, parent, row):
        """Create input parameters section"""
        # Section frame
        section = ttk.LabelFrame(parent, text="Input Parameters", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        section.columnconfigure(1, weight=1)
        
        # Video file selection
        ttk.Label(section, text="Video File:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.video_path_var = tk.StringVar()
        video_entry = ttk.Entry(section, textvariable=self.video_path_var, width=50)
        video_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        ttk.Button(section, text="Browse...", command=self.browse_video).grid(
            row=0, column=2, pady=2
        )
        
        # Hardware profile
        ttk.Label(section, text="Hardware Profile:").grid(row=1, column=0, sticky=tk.W, pady=2)
        profile_frame = ttk.Frame(section)
        profile_frame.grid(row=1, column=1, sticky=tk.W, columnspan=2, pady=2)
        
        self.profile_var = tk.StringVar(value="laptop")
        profiles = ["laptop", "pc", "custom"]
        for i, profile in enumerate(profiles):
            rb = ttk.Radiobutton(
                profile_frame,
                text=profile.capitalize(),
                variable=self.profile_var,
                value=profile,
                command=self.on_profile_change
            )
            rb.grid(row=0, column=i, padx=5)
        
        # Profile description
        self.profile_desc_var = tk.StringVar()
        ttk.Label(section, textvariable=self.profile_desc_var, font=("TkDefaultFont", 8)).grid(
            row=2, column=1, sticky=tk.W, columnspan=2, pady=2
        )
        
        # LM Studio configuration
        ttk.Separator(section, orient=tk.HORIZONTAL).grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
        )
        ttk.Label(section, text="LM Studio Configuration", font=("TkDefaultFont", 9, "bold")).grid(
            row=4, column=0, columnspan=3, sticky=tk.W, pady=2
        )
        
        # LM Studio URL
        ttk.Label(section, text="LM Studio URL:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.lm_studio_url_var = tk.StringVar(
            value=os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
        )
        ttk.Entry(section, textvariable=self.lm_studio_url_var, width=50).grid(
            row=5, column=1, sticky=(tk.W, tk.E), padx=5, pady=2, columnspan=2
        )
        
        # Text model
        ttk.Label(section, text="Text Model:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.text_model_var = tk.StringVar(value=os.getenv("LM_STUDIO_MODEL", "phi-3-mini"))
        ttk.Entry(section, textvariable=self.text_model_var, width=50).grid(
            row=6, column=1, sticky=(tk.W, tk.E), padx=5, pady=2, columnspan=2
        )
        
        # Vision model
        ttk.Label(section, text="Vision Model:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.vision_model_var = tk.StringVar(value=os.getenv("LM_STUDIO_VISION_MODEL", "llava-7b-q4"))
        ttk.Entry(section, textvariable=self.vision_model_var, width=50).grid(
            row=7, column=1, sticky=(tk.W, tk.E), padx=5, pady=2, columnspan=2
        )
        
        # Whisper model
        ttk.Label(section, text="Whisper Model:").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.whisper_model_var = tk.StringVar(value=os.getenv("WHISPER_MODEL", "small"))
        whisper_combo = ttk.Combobox(
            section,
            textvariable=self.whisper_model_var,
            values=["tiny", "base", "small", "medium", "large"],
            state="readonly",
            width=15
        )
        whisper_combo.grid(row=8, column=1, sticky=tk.W, padx=5, pady=2)
        
        return row + 1
    
    def create_project_section(self, parent, row):
        """Create project settings section"""
        section = ttk.LabelFrame(parent, text="Project Settings", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        section.columnconfigure(1, weight=1)
        
        # Project name
        ttk.Label(section, text="Project Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.project_name_var = tk.StringVar(value="Meeting Project")
        ttk.Entry(section, textvariable=self.project_name_var, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2, columnspan=2
        )
        
        # Output directory
        ttk.Label(section, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.output_dir_var = tk.StringVar(value="./output")
        ttk.Entry(section, textvariable=self.output_dir_var, width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2
        )
        ttk.Button(section, text="Browse...", command=self.browse_output).grid(
            row=1, column=2, pady=2
        )
        
        return row + 1
    
    def create_frame_extraction_section(self, parent, row):
        """Create frame extraction options section"""
        section = ttk.LabelFrame(parent, text="Frame Extraction Options", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        section.columnconfigure(1, weight=1)
        
        # Use key frames
        self.use_key_frames_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            section,
            text="Use Key Frames (scene change detection)",
            variable=self.use_key_frames_var,
            command=self.on_key_frames_toggle
        ).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=2)
        
        # Extraction interval
        ttk.Label(section, text="Extraction Interval (seconds):").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.interval_var = tk.IntVar(value=10)
        self.interval_spinbox = ttk.Spinbox(
            section,
            from_=1,
            to=60,
            textvariable=self.interval_var,
            width=10,
            state="disabled"
        )
        self.interval_spinbox.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Max key frames
        ttk.Label(section, text="Max Key Frames:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.max_key_frames_var = tk.IntVar(value=15)
        ttk.Spinbox(
            section,
            from_=1,
            to=100,
            textvariable=self.max_key_frames_var,
            width=10
        ).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Max frames to analyze
        ttk.Label(section, text="Max Frames to Analyze:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.max_frames_analyze_var = tk.IntVar(value=10)
        ttk.Spinbox(
            section,
            from_=1,
            to=50,
            textvariable=self.max_frames_analyze_var,
            width=10
        ).grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        return row + 1
    
    def create_progress_section(self, parent, row):
        """Create progress and status section"""
        section = ttk.LabelFrame(parent, text="Progress and Status", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        section.columnconfigure(0, weight=1)
        section.rowconfigure(2, weight=1)
        
        # Progress bar
        ttk.Label(section, text="Progress:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            section,
            variable=self.progress_var,
            maximum=100,
            mode="determinate"
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to analyze")
        status_label = ttk.Label(
            section,
            textvariable=self.status_var,
            font=("TkDefaultFont", 9, "bold")
        )
        status_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Log area
        ttk.Label(section, text="Detailed Log:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.log_text = scrolledtext.ScrolledText(
            section,
            height=15,
            width=80,
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        self.log_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=2)
        
        # Configure text tags for colored output
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("info", foreground="blue")
        
        return row + 1
    
    def create_control_buttons(self, parent, row):
        """Create control buttons section"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=10)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)
        
        # Start button
        self.start_button = ttk.Button(
            button_frame,
            text="Start Analysis",
            command=self.start_analysis,
            style="Accent.TButton"
        )
        self.start_button.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))
        
        # Stop button
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop Analysis",
            command=self.stop_analysis,
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        # Clear log button
        self.clear_button = ttk.Button(
            button_frame,
            text="Clear Log",
            command=self.clear_log
        )
        self.clear_button.grid(row=0, column=2, padx=5, sticky=(tk.W, tk.E))
        
        # Open output folder button
        self.open_output_button = ttk.Button(
            button_frame,
            text="Open Output Folder",
            command=self.open_output_folder
        )
        self.open_output_button.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        return row + 1
    
    def create_results_section(self, parent, row):
        """Create results section"""
        section = ttk.LabelFrame(parent, text="Generated Files", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        section.columnconfigure(1, weight=1)
        
        # SRS Markdown
        ttk.Label(section, text="SRS (Markdown):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.srs_markdown_var = tk.StringVar(value="Not generated yet")
        ttk.Label(section, textvariable=self.srs_markdown_var, foreground="gray").grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=2
        )
        self.srs_markdown_button = ttk.Button(
            section,
            text="Open",
            command=lambda: self.open_file(self.results.get("srs_markdown")),
            state="disabled"
        )
        self.srs_markdown_button.grid(row=0, column=2, padx=5, pady=2)
        
        # SRS DOCX
        ttk.Label(section, text="SRS (DOCX):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.srs_docx_var = tk.StringVar(value="Not generated yet")
        ttk.Label(section, textvariable=self.srs_docx_var, foreground="gray").grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=2
        )
        self.srs_docx_button = ttk.Button(
            section,
            text="Open",
            command=lambda: self.open_file(self.results.get("srs_docx")),
            state="disabled"
        )
        self.srs_docx_button.grid(row=1, column=2, padx=5, pady=2)
        
        # Requirements JSON
        ttk.Label(section, text="Requirements (JSON):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.requirements_json_var = tk.StringVar(value="Not generated yet")
        ttk.Label(section, textvariable=self.requirements_json_var, foreground="gray").grid(
            row=2, column=1, sticky=tk.W, padx=5, pady=2
        )
        self.requirements_json_button = ttk.Button(
            section,
            text="Open",
            command=lambda: self.open_file(self.results.get("requirements_json")),
            state="disabled"
        )
        self.requirements_json_button.grid(row=2, column=2, padx=5, pady=2)
        
        return row + 1
    
    def browse_video(self):
        """Open file browser for video selection"""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mov *.mkv *.webm"),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.video_path_var.set(filename)
    
    def browse_output(self):
        """Open directory browser for output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
    
    def on_profile_change(self):
        """Handle hardware profile change"""
        profile = self.profile_var.get()
        if profile == "custom":
            self.profile_desc_var.set("Custom settings - configure models manually")
        else:
            desc = get_profile_description(profile)
            self.profile_desc_var.set(f"{desc}")
    
    def on_key_frames_toggle(self):
        """Handle key frames checkbox toggle"""
        if self.use_key_frames_var.get():
            self.interval_spinbox.config(state="disabled")
        else:
            self.interval_spinbox.config(state="normal")
    
    def clear_log(self):
        """Clear the log text area"""
        self.log_text.delete(1.0, tk.END)
    
    def log_message(self, message, tag=None):
        """Add a message to the log"""
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.update_idletasks()
    
    def update_progress(self, step, total_steps, message, error=None):
        """Update progress bar and status"""
        # Calculate percentage
        percent = (step / total_steps) * 100
        self.progress_var.set(percent)
        
        # Update status
        if error:
            self.status_var.set(f"Error: {message}")
            self.log_message(f"ERROR: {message} - {error}", "error")
        else:
            self.status_var.set(message)
            self.log_message(message, "info")
    
    def show_error(self, error_message):
        """Display error in GUI"""
        self.status_var.set(f"Error: {error_message}")
        self.log_message(f"ERROR: {error_message}", "error")
        messagebox.showerror("Error", error_message)
    
    def start_analysis(self):
        """Start the analysis in a background thread"""
        # Validate inputs
        video_path = self.video_path_var.get()
        if not video_path:
            self.show_error("Please select a video file")
            return
        
        if not os.path.exists(video_path):
            self.show_error(f"Video file not found: {video_path}")
            return
        
        # Reset state
        self.stop_requested = False
        self.results = {}
        
        # Update UI state
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress_var.set(0)
        self.status_var.set("Starting analysis...")
        
        # Clear previous results
        self.srs_markdown_var.set("Not generated yet")
        self.srs_docx_var.set("Not generated yet")
        self.requirements_json_var.set("Not generated yet")
        self.srs_markdown_button.config(state="disabled")
        self.srs_docx_button.config(state="disabled")
        self.requirements_json_button.config(state="disabled")
        
        # Start analysis thread
        self.analysis_thread = threading.Thread(target=self._run_analysis, daemon=True)
        self.analysis_thread.start()
    
    def stop_analysis(self):
        """Request to stop the ongoing analysis"""
        self.stop_requested = True
        self.status_var.set("Stopping analysis...")
        self.log_message("Stop requested by user", "info")
    
    def _run_analysis(self):
        """Run analysis in background thread"""
        try:
            # Get configuration from GUI
            video_path = self.video_path_var.get()
            output_dir = self.output_dir_var.get()
            project_name = self.project_name_var.get()
            lm_studio_url = self.lm_studio_url_var.get()
            text_model = self.text_model_var.get()
            vision_model = self.vision_model_var.get()
            whisper_model = self.whisper_model_var.get()
            
            # Get profile settings
            profile = self.profile_var.get()
            vision_on_cpu = False
            if profile == "laptop":
                vision_on_cpu = True
            elif profile == "pc":
                vision_on_cpu = False
            
            # Create analyzer with progress callback
            self.analyzer = MeetingAnalyzer(
                video_path=video_path,
                lm_studio_url=lm_studio_url,
                text_model=text_model,
                vision_model=vision_model,
                whisper_model=whisper_model,
                vision_on_cpu=vision_on_cpu,
                output_dir=output_dir,
                progress_callback=self._progress_callback
            )
            
            # Run analysis with frame extraction settings
            results = self.analyzer.analyze(
                extract_frames_interval=self.interval_var.get(),
                extract_key_frames=self.use_key_frames_var.get(),
                max_key_frames=self.max_key_frames_var.get(),
                max_frames_to_analyze=self.max_frames_analyze_var.get(),
                project_name=project_name
            )
            
            # Check if stopped
            if self.stop_requested:
                self.message_queue.put(("status", "Analysis stopped by user"))
                self.message_queue.put(("stopped", None))
                return
            
            # Send completion message
            self.message_queue.put(("complete", results))
            
        except Exception as e:
            # Send error message
            self.message_queue.put(("error", str(e)))
    
    def _progress_callback(self, step, total_steps, message, error=None):
        """Progress callback for analyzer (called from background thread)"""
        # Check if stop requested
        if self.stop_requested:
            raise InterruptedError("Analysis stopped by user")
        
        # Send progress update to main thread
        self.message_queue.put(("progress", (step, total_steps, message, error)))
    
    def process_queue(self):
        """Process messages from background thread"""
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                
                if msg_type == "progress":
                    step, total_steps, message, error = data
                    self.update_progress(step, total_steps, message, error)
                
                elif msg_type == "complete":
                    self.analysis_complete(data)
                
                elif msg_type == "error":
                    self.analysis_error(data)
                
                elif msg_type == "stopped":
                    self.analysis_stopped()
                
                elif msg_type == "status":
                    self.log_message(data, "info")
        
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_queue)
    
    def analysis_complete(self, results):
        """Handle analysis completion"""
        self.results = results
        
        # Update UI state
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.progress_var.set(100)
        self.status_var.set("Analysis complete!")
        
        # Log success
        self.log_message("=" * 60, "success")
        self.log_message("ANALYSIS COMPLETE", "success")
        self.log_message("=" * 60, "success")
        
        # Update results section
        if "srs_markdown" in results:
            self.srs_markdown_var.set(results["srs_markdown"])
            self.srs_markdown_button.config(state="normal")
            self.log_message(f"✓ SRS Markdown: {results['srs_markdown']}", "success")
        
        if "srs_docx" in results:
            self.srs_docx_var.set(results["srs_docx"])
            self.srs_docx_button.config(state="normal")
            self.log_message(f"✓ SRS DOCX: {results['srs_docx']}", "success")
        
        if "requirements_json" in results:
            self.requirements_json_var.set(results["requirements_json"])
            self.requirements_json_button.config(state="normal")
            self.log_message(f"✓ Requirements JSON: {results['requirements_json']}", "success")
        
        # Show completion dialog
        messagebox.showinfo(
            "Analysis Complete",
            "Meeting analysis completed successfully!\n\nGenerated files are available in the Results section."
        )
    
    def analysis_error(self, error_message):
        """Handle analysis error"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_var.set(f"Analysis failed: {error_message}")
        self.log_message("=" * 60, "error")
        self.log_message(f"ANALYSIS FAILED: {error_message}", "error")
        self.log_message("=" * 60, "error")
        
        messagebox.showerror("Analysis Failed", f"An error occurred:\n\n{error_message}")
    
    def analysis_stopped(self):
        """Handle analysis stopped by user"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_var.set("Analysis stopped")
        self.log_message("Analysis stopped by user", "info")
    
    def open_file(self, filepath):
        """Open a file with the system default application"""
        if not filepath or not os.path.exists(filepath):
            messagebox.showerror("Error", "File not found")
            return
        
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", filepath])
            elif platform.system() == "Windows":
                os.startfile(filepath)
            else:  # Linux
                subprocess.run(["xdg-open", filepath])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")
    
    def open_output_folder(self):
        """Open the output directory in file explorer"""
        output_dir = self.output_dir_var.get()
        
        # Create directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", output_dir])
            elif platform.system() == "Windows":
                os.startfile(output_dir)
            else:  # Linux
                subprocess.run(["xdg-open", output_dir])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder:\n{str(e)}")
    
    def load_settings(self):
        """Load saved settings from environment or config file"""
        # Update profile description
        self.on_profile_change()
        
        # Set initial state of interval spinbox
        self.on_key_frames_toggle()
    
    def save_settings(self):
        """Save current settings to config file (optional)"""
        # This could be implemented to save to a JSON config file
        pass


def main():
    """Entry point for GUI application"""
    root = tk.Tk()
    app = MeetingAnalyzerGUI(root)
    
    # Handle window close
    def on_closing():
        if app.analysis_thread and app.analysis_thread.is_alive():
            if messagebox.askokcancel("Quit", "Analysis is running. Do you want to quit?"):
                app.stop_requested = True
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start main loop
    root.mainloop()


if __name__ == "__main__":
    main()
