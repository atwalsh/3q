# QQQ

Easily share your current git branch with users on GitHub.

### Install
```bash
pip install 3q
```

### Requirements
- A GitHub Personal Access Token with `repo` permissions

### How-to
1. Run `qqq login` to configure QQQ:
   ```bash
   qqq login -u atwalsh -t TOKEN
   ```

2. Change directories to the git repository you want to share
3. Checkout the branch you want to share
4. Run `qqq send` to make a new private repository on GitHub:
   ```bash
   # Share the currently checked out branch with 
   # GitHub user `atwalsh`
   
   qqq send atwalsh
   ``` 
   
### Options
#### `send`
- `-a` Adds an additional admin collaborator to the GitHub repository
  - Send multiple `-a` options to add multiple admin collaborators:
    ```bash
    # Send branch to `atwalsh`, add `MedShift` and `GridResearch` 
    # as admin collaborators
    
    qqq send atwalsh -a MedShift -a GridResearch
    ```

### Inspiration
[a], [b], [c]

[a]: https://www.reddit.com/r/wallstreetbets/comments/f7xj7e/based_on_fridays_post_the_sub_has_lost_around/
[b]: https://www.reddit.com/r/wallstreetbets/comments/9qe256/someone_mentioned_my_last_play_wasnt_a_true_fd/
[c]: https://www.reddit.com/r/wallstreetbets/comments/7uu2lk/when_qqq_dips_1/
