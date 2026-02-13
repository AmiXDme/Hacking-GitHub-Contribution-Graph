"""
Git operations for creating backdated commits
"""

import os
import json
from datetime import datetime, timedelta
from git import Repo, Actor


def calculate_date(weeks, days):
    """Calculate date based on weeks and days offset from one year ago"""
    one_year_ago = datetime.now() - timedelta(days=365)
    target_date = one_year_ago + timedelta(weeks=weeks, days=days+1)
    return target_date


def initialize_repo(repo_url, target_dir):
    """
    Initialize or clone a repository
    """
    # Create directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    
    # Check if it's already a repo
    git_dir = os.path.join(target_dir, '.git')
    
    if os.path.exists(git_dir):
        repo = Repo(target_dir)
        
        # Update remote
        if 'origin' in [remote.name for remote in repo.remotes]:
            repo.delete_remote('origin')
        repo.create_remote('origin', repo_url)
    else:
        # Initialize new repo
        repo = Repo.init(target_dir)
        repo.create_remote('origin', repo_url)
        
        # Create initial data file
        data_file = os.path.join(target_dir, 'data.json')
        with open(data_file, 'w') as f:
            json.dump({}, f)
    
    return repo


def mark_commit(repo, week, day, intensity=1, message=None, author_name=None, author_email=None):
    """
    Create a commit (or multiple for intensity) at a specific coordinate
    """
    target_date = calculate_date(week, day)
    data_file = os.path.join(repo.working_dir, 'data.json')
    
    # Write data
    data = {
        'date': target_date.isoformat(),
        'week': week,
        'day': day
    }
    
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Stage the file
    repo.index.add(['data.json'])
    
    # Create commits (intensity times)
    for i in range(intensity):
        commit_message = message or f"{target_date.isoformat()} ({week},{day})"
        
        # Set author if provided
        if author_name and author_email:
            author = Actor(author_name, author_email)
            repo.index.commit(commit_message, author=author, committer=author, author_date=target_date, commit_date=target_date)
        else:
            # Use git config default
            repo.index.commit(commit_message, author_date=target_date, commit_date=target_date)



def create_pattern_commits(repo, coordinates, intensity=1, progress_callback=None, author_name=None, author_email=None):
    """
    Create commits from pattern coordinates
    """
    total = len(coordinates)
    
    for i, coord in enumerate(coordinates):
        week = coord['week']
        day = coord['day']
        char = coord['char']
        
        message = f"Pattern: {char} ({week},{day})"
        mark_commit(repo, week, day, intensity, message, author_name, author_email)
        
        if progress_callback:
            progress_callback({
                'current': i + 1,
                'total': total,
                'week': week,
                'day': day,
                'char': char,
                'percentage': round(((i + 1) / total) * 100)
            })
    
    # Push to remote
    try:
        origin = repo.remote('origin')
        
        # Get current branch or default to 'main'
        if repo.head.is_detached or not repo.heads:
            # Create main branch if it doesn't exist
            if 'main' not in [h.name for h in repo.heads]:
                repo.create_head('main')
            repo.heads.main.checkout()
            current_branch = 'main'
        else:
            current_branch = repo.active_branch.name
        
        # Push with force to handle first push
        origin.push(refspec=f'{current_branch}:{current_branch}', force=True)
    except Exception as e:
        raise Exception(f"Failed to push to remote: {str(e)}")

