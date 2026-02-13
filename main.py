"""
GitHub Contribution Artist - Main GUI Application
Create beautiful text patterns on your GitHub contribution graph
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os
from pattern_calculator import (
    text_to_pattern, validate_text, get_pattern_stats,
    preview_pattern, get_max_characters
)
from git_bot import initialize_repo, create_pattern_commits


class GitHubContributionArtist:
    def __init__(self, root):
        self.root = root
        self.root.title("Hacking GitHub Contribution Graph")
        self.root.geometry("900x750")
        self.root.configure(bg='#0d1117')
        
        # Variables
        self.repo_url = tk.StringVar()
        self.text_input = tk.StringVar()
        self.intensity = tk.IntVar(value=1)
        self.is_running = False
        
        # Setup UI
        self.setup_ui()
        
        # Bind text input changes
        self.text_input.trace('w', self.on_text_change)
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Main container with padding
        main_frame = tk.Frame(self.root, bg='#0d1117', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(
            main_frame,
            text="🎨 GitHub Contribution Artist",
            font=('Segoe UI', 24, 'bold'),
            bg='#0d1117',
            fg='#58a6ff'
        )
        title.pack(pady=(0, 20))
        
        # Repository URL
        url_frame = tk.Frame(main_frame, bg='#0d1117')
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        url_label = tk.Label(
            url_frame,
            text="Repository URL:",
            font=('Segoe UI', 11),
            bg='#0d1117',
            fg='#c9d1d9'
        )
        url_label.pack(anchor=tk.W, pady=(0, 5))
        
        url_entry = tk.Entry(
            url_frame,
            textvariable=self.repo_url,
            font=('Segoe UI', 11),
            bg='#161b22',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            relief=tk.FLAT,
            bd=2
        )
        url_entry.pack(fill=tk.X, ipady=8, ipadx=10)
        url_entry.insert(0, "https://github.com/username/repo.git")
        
        # Text Input
        text_frame = tk.Frame(main_frame, bg='#0d1117')
        text_frame.pack(fill=tk.X, pady=(0, 15))
        
        text_label = tk.Label(
            text_frame,
            text=f"Text to Draw (Max {get_max_characters()} characters):",
            font=('Segoe UI', 11),
            bg='#0d1117',
            fg='#c9d1d9'
        )
        text_label.pack(anchor=tk.W, pady=(0, 5))
        
        text_entry = tk.Entry(
            text_frame,
            textvariable=self.text_input,
            font=('Segoe UI', 16, 'bold'),
            bg='#161b22',
            fg='#58a6ff',
            insertbackground='#58a6ff',
            relief=tk.FLAT,
            bd=2
        )
        text_entry.pack(fill=tk.X, ipady=12, ipadx=10)
        text_entry.insert(0, "HELLO")
        
        # Stats display
        self.stats_label = tk.Label(
            text_frame,
            text="",
            font=('Segoe UI', 9),
            bg='#0d1117',
            fg='#8b949e',
            justify=tk.LEFT
        )
        self.stats_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Intensity slider
        intensity_frame = tk.Frame(main_frame, bg='#0d1117')
        intensity_frame.pack(fill=tk.X, pady=(0, 15))
        
        intensity_label = tk.Label(
            intensity_frame,
            text="Commit Intensity (commits per pixel for darker color):",
            font=('Segoe UI', 11),
            bg='#0d1117',
            fg='#c9d1d9'
        )
        intensity_label.pack(anchor=tk.W, pady=(0, 5))
        
        intensity_slider_frame = tk.Frame(intensity_frame, bg='#0d1117')
        intensity_slider_frame.pack(fill=tk.X)
        
        self.intensity_value_label = tk.Label(
            intensity_slider_frame,
            text="1",
            font=('Segoe UI', 11, 'bold'),
            bg='#0d1117',
            fg='#58a6ff',
            width=3
        )
        self.intensity_value_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        intensity_slider = tk.Scale(
            intensity_slider_frame,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.intensity,
            command=self.on_intensity_change,
            bg='#161b22',
            fg='#c9d1d9',
            activebackground='#238636',
            troughcolor='#0d1117',
            highlightthickness=0,
            relief=tk.FLAT,
            showvalue=0
        )
        intensity_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Preview Canvas
        preview_frame =tk.LabelFrame(
            main_frame,
            text=" Pattern Preview ",
            font=('Segoe UI', 11, 'bold'),
            bg='#0d1117',
            fg='#58a6ff',
            bd=2,
            relief=tk.GROOVE
        )
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.canvas = tk.Canvas(
            preview_frame,
            bg='#010409',
            highlightthickness=0,
            height=150
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control Buttons
        button_frame = tk.Frame(main_frame, bg='#0d1117')
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.generate_btn = tk.Button(
            button_frame,
            text="🚀 Generate Pattern",
            font=('Segoe UI', 12, 'bold'),
            bg='#238636',
            fg='white',
            activebackground='#2ea043',
            activeforeground='white',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2',
            command=self.start_generation
        )
        self.generate_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ Stop",
            font=('Segoe UI', 12, 'bold'),
            bg='#da3633',
            fg='white',
            activebackground='#f85149',
            activeforeground='white',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2',
            command=self.stop_generation,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='determinate',
            length=300
        )
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Logs
        logs_frame = tk.LabelFrame(
            main_frame,
            text=" Logs ",
            font=('Segoe UI', 11, 'bold'),
            bg='#0d1117',
            fg='#58a6ff',
            bd=2,
            relief=tk.GROOVE
        )
        logs_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            logs_frame,
            height=10,
            font=('Consolas', 9),
            bg='#010409',
            fg='#8b949e',
            insertbackground='#58a6ff',
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initial update
        self.on_text_change()
    
    def on_text_change(self, *args):
        """Called when text input changes"""
        text = self.text_input.get()
        
        if not text:
            self.stats_label.config(text="")
            self.canvas.delete('all')
            return
        
        # Validate
        valid, message = validate_text(text)
        
        if valid:
            stats = get_pattern_stats(text)
            self.stats_label.config(
                text=f"✓ {stats['characters']} chars | {stats['commits']} commits | {stats['weeks']} weeks",
                fg='#3fb950'
            )
            self.draw_preview(text)
        else:
            self.stats_label.config(text=f"✗ {message}", fg='#f85149')
            self.canvas.delete('all')
    
    def on_intensity_change(self, value):
        """Called when intensity slider changes"""
        self.intensity_value_label.config(text=str(value))
    
    def draw_preview(self, text):
        """Draw pattern preview on canvas"""
        self.canvas.delete('all')
        
        grid = preview_pattern(text)
        if not grid:
            return
        
        rows = len(grid)
        cols = len(grid[0]) if grid else 0
        
        # Calculate cell size to fit canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:  # Not drawn yet
            canvas_width = 800
            canvas_height = 150
        
        cell_width = max(3, min(15, (canvas_width - 20) // cols))
        cell_height = max(3, min(15, (canvas_height - 20) // rows))
        cell_size = min(cell_width, cell_height)
        
        # Center the grid
        start_x = (canvas_width - (cols * (cell_size + 2))) // 2
        start_y = (canvas_height - (rows * (cell_size + 2))) // 2
        
        # Draw grid
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (cell_size + 2)
                y = start_y + row * (cell_size + 2)
                
                color = '#39d353' if grid[row][col] == 1 else '#161b22'
                
                self.canvas.create_rectangle(
                    x, y,
                    x + cell_size, y + cell_size,
                    fill=color,
                    outline='#0d1117',
                    width=1
                )
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_generation(self):
        """Start pattern generation"""
        repo_url = self.repo_url.get().strip()
        text = self.text_input.get().strip()
        
        if not repo_url:
            messagebox.showerror("Error", "Please enter a repository URL")
            return
        
        if not text:
            messagebox.showerror("Error", "Please enter text to draw")
            return
        
        # Validate text
        valid, message = validate_text(text)
        if not valid:
            messagebox.showerror("Error", message)
            return
        
        # Disable controls
        self.generate_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.is_running = True
        
        # Clear logs and reset progress
        self.log_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        
        # Start in thread
        thread = threading.Thread(target=self.run_generation, args=(repo_url, text))
        thread.daemon = True
        thread.start()
    
    def run_generation(self, repo_url, text):
        """Run the generation process"""
        try:
            self.log(f"🎨 Creating pattern: '{text}'")
            self.log(f"📦 Repository: {repo_url}")
            self.log(f"💪 Intensity: {self.intensity.get()} commits/pixel\n")
            
            # Get pattern
            coordinates = text_to_pattern(text)
            total = len(coordinates)
            
            self.log(f"📊 Pattern statistics:")
            self.log(f"   - Text: {text}")
            self.log(f"   - Commits needed: {total}")
            self.log(f"   - Intensity: {self.intensity.get()}x")
            self.log(f"   - Total commits: {total * self.intensity.get()}\n")
            
            # Initialize repo
            target_dir = os.path.join(os.path.expanduser('~'), 'github-contribution-repo')
            self.log(f"📂 Initializing repository at: {target_dir}")
            
            repo = initialize_repo(repo_url, target_dir)
            self.log(f"✓ Repository initialized\n")
            
            # Create commits
            self.log("🚀 Starting commit generation...\n")
            
            def progress_callback(progress):
                if not self.is_running:
                    raise Exception("Generation stopped by user")
                
                self.progress['value'] = progress['percentage']
                self.log(f"[{progress['current']}/{progress['total']}] '{progress['char']}' at Week {progress['week']}, Day {progress['day']}")
            
            create_pattern_commits(
                repo,
                coordinates,
                self.intensity.get(),
                progress_callback
            )
            
            self.log(f"\n✅ Pattern '{text}' created successfully!")
            self.log(f"📁 Repository location: {target_dir}")
            self.log("\n⚠️ Don't forget to:")
            self.log("1. Enable 'Private contributions' in your GitHub profile settings")
            self.log("2. Wait a few minutes for GitHub to update your contribution graph")
            
            messagebox.showinfo("Success", f"Pattern '{text}' created successfully!\n\nCheck your GitHub profile in a few minutes.")
            
        except Exception as e:
            self.log(f"\n❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to create pattern:\n{str(e)}")
        
        finally:
            self.generate_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.is_running = False
            self.progress['value'] = 0
    
    def stop_generation(self):
        """Stop the generation process"""
        self.is_running = False
        self.log("\n⏹ Stopping generation...")


def main():
    root = tk.Tk()
    app = GitHubContributionArtist(root)
    root.mainloop()


if __name__ == '__main__':
    main()
