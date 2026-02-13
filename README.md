# 🎨 Hacking GitHub Contribution Graph

**Create beautiful text patterns on your GitHub contribution graph!**

A Python GUI application that automates GitHub commits to draw text patterns (like "HELLO", "2026", or your name) on your GitHub contribution graph using backdated commits.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-Educational-orange.svg)

## ✨ Features

- 🎯 **Text-to-Pattern**: Type any text and see it previewed on the contribution grid
- 📊 **Real-time Preview**: Visual preview showing exactly how your pattern will look
- 💪 **Intensity Control**: Adjust commits per pixel (1-10) for darker green squares
- ⚡ **Character Validation**: Automatically validates text length (max 8-9 characters)
- 📈 **Progress Tracking**: Real-time logs and progress bar
- 🎨 **Modern Dark UI**: Beautiful GitHub-themed interface
- 🔒 **No Login Required**: Uses your existing Git credentials

## 🖼️ Screenshots

```
┌─────────────────────────────────────────────┐
│   🎨 Hacking GitHub Contribution Graph      │
├─────────────────────────────────────────────┤
│ Repository URL:                             │
│ https://github.com/AmiXDme/Hacking-GitHub-Contribution-Graph.git │

│                                             │
│ Text to Draw (Max 8 characters):            │
│ HELLO                                       │
│ ✓ 5 chars | 120 commits | 29 weeks         │
│                                             │
│ Commit Intensity: ▓▓▓░░░░░░░ 3             │
│                                             │
│ ┌─── Pattern Preview ───────────────────┐  │
│ │  ██ ██     ██ ██  ██     ██     ███    │  │
│ │  ██ ██ ██  ██ ██     ██        ██ ██   │  │
│ │  ██ ██ ██  ██ ██     ██        ██ ██   │  │
│ │  ███  ██ ██ ██ ██     ██        ██ ██  │  │
│ │  ██ ██ ██  ██ ██     ██        ██ ██   │  │
│ │  ██ ██ ██  ██ ██     ██        ██ ██   │  │
│ │  ██ ██     ██ ███ ███ ███       ███    │  │
│ └───────────────────────────────────────┘  │
│                                             │
│  [🚀 Generate Pattern]      [⏹ Stop]       │
│  Progress: ████████░░░░░░░░░░ 45%          │
│                                             │
│  ┌─── Logs ────────────────────────────┐   │
│  │ 🎨 Creating pattern: 'HELLO'       │   │
│  │ [45/120] 'L' at Week 15, Day 3     │   │
│  └────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** installed
- **uv** package manager ([Install uv](https://github.com/astral-sh/uv))
- **Git** configured with credentials
- **A Private GitHub Repository**

### Installation

1. **Clone or Download** this project

2. **Create virtual environment**:
   ```bash
   uv venv
   ```

3. **Install dependencies**:
   ```bash
   .venv\Scripts\activate
   uv pip install gitpython
   ```

### Running the Application

**Windows:**
```bash
run.bat
```

**Or manually:**
```bash
.venv\Scripts\activate
python main.py
```

## 📖 How to Use

### Step 1: Prepare Your Repository

1. Create a **NEW PRIVATE** repository on GitHub
2. Copy the repository URL (e.g., `https://github.com/username/my-art.git`)

> ⚠️ **Important**: Use a NEW, EMPTY private repository. Don't use existing projects!

### Step 2: Configure the App

1. Launch the application (`run.bat`)
2. **Paste Repository URL** in the first field
3. **Type your text** (e.g., "HELLO", "2026", "LOVE")
   - Maximum 8-9 characters (GitHub graph is 53 weeks wide)
   - Supports A-Z, 0-9, and some symbols (!, ?, +, -, .)
4. **Adjust Intensity** slider (1-10 commits per pixel)
   - 1 = Light green
   - 5-7 = Medium green
   - 10 = Dark green

### Step 3: Preview & Generate

1. **Preview** automatically shows your pattern
2. **Click "Generate Pattern"**
3. **Watch the progress** in real-time
4. **Wait for completion** (can take a few minutes depending on text length)

### Step 4: View on GitHub

1. Go to your **GitHub profile**
2. Click **"Contribution settings"** (above the graph)
3. Enable **"Private contributions"** checkbox
4. **Refresh** the page - your pattern should appear!

> ⏰ **Note**: GitHub may take 5-10 minutes to update the contribution graph.

## 🎯 Technical Details

### How It Works

1. **Text Conversion**: Converts each character to a 5×7 pixel pattern using a custom font
2. **Date Calculation**: Maps each pixel to a specific date (week, day) one year ago
3. **Backdated Commits**: Uses Git's `--date` flag to create commits at calculated dates
4. **Intensity Multiplier**: Creates multiple commits per pixel for darker colors

### Grid Specifications

- **GitHub Graph**: 7 rows (Sun-Sat) × 53 columns (weeks)
- **Character Size**: 5 pixels wide × 7 pixels tall
- **Spacing**: 1 week between characters
- **Maximum Text**: 8-9 characters (depends on character width)

### Files Created

```
C:\Users\YourName\github-contribution-repo\
├── .git\               # Git repository
└── data.json           # Modified with each commit
```

## ⚙️ Configuration

### Change Commit Intensity

Use the slider in the GUI (1-10):
- **1**: Minimal green (1 commit/pixel)
- **3-5**: Medium green (good balance)
- **10**: Maximum green (10 commits/pixel)

### Supported Characters

- **Letters**: A-Z (automatically converted to uppercase)
- **Numbers**: 0-9
- **Symbols**: Space, !, ?, +, -, .
- **Future**: Add custom characters in `fonts.py`

## ⚠️ Important Notes

### GitHub Requirements

✅ **Must use a PRIVATE repository**
✅ **Enable "Private contributions" in profile settings**
✅ **Git credentials must be configured** (`git config user.name` and `user.email`)
✅ **Wait 5-10 minutes** for GitHub to update the graph

### Ethical Use

This project is for:
- ✅ **Learning** how Git metadata works
- ✅ **Artistic expression** and fun experiments
- ✅ **Educational purposes**

**NOT** for:
- ❌ Deceiving employers or recruiters
- ❌ Faking open-source contributions
- ❌ Misrepresenting your actual coding activity

> 💡 **Tip**: Senior developers can easily spot these patterns. Use for art, not deception!

## 🛠️ Development

### Project Structure

```
Hacking GitHub Contribution Graph/
├── main.py                 # GUI application
├── fonts.py                # 5×7 pixel font definitions
├── pattern_calculator.py   # Text-to-grid mapping
├── git_bot.py             # Git operations & backdating
├── requirements.txt        # Python dependencies
├── run.bat                # Windows run script
├── .venv/                 # Virtual environment
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

### Adding Custom Characters

Edit `fonts.py` and add your character:

```python
FONTS = {
    '❤': [
        [0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]
}
```

## 🐛 Troubleshooting

### "Module not found" error
```bash
# Reinstall dependencies
.venv\Scripts\activate
uv pip install gitpython
```

### "Authentication failed"
```bash
# Configure Git credentials
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Pattern doesn't show on GitHub
1. Enable "Private contributions" in GitHub settings
2. Wait 10-15 minutes
3. Hard refresh the page (Ctrl+F5)
4. Check the repository has commits (`git log`)

### Text exceeds limit
- Maximum 8-9 characters
- Use shorter text or abbreviations
- Remove spaces to fit more letters

## 📊 Example Patterns

```
"HELLO"  → 5 chars, ~120 commits, 29 weeks
"2026"   → 4 chars, ~96 commits,  23 weeks  
"CODE"   → 4 chars, ~96 commits,  23 weeks
"AI"     → 2 chars, ~48 commits,  11 weeks
"LOVE ❤" → 6 chars, ~144 commits, 35 weeks
```

## 📜 License

**Educational Use Only**

This project is provided for learning and artistic purposes. Use responsibly.

## 🙏 Credits

Created with:
- **Python** - Programming language
- **Tkinter** - GUI framework
- **GitPython** - Git operations
- **uv** - Fast Python package installer

---

**Happy Contribution Crafting! 🎨✨**

> ⭐ Star this repo if you created something cool!
