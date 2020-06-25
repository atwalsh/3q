# QQQ

Easily share your current git branch with users on GitHub. 

### Requirements
- A GitHub Personal Access Token with `repo` permissions

### How-to
1. Run `qqq login` to configure QQQ:
   ```bash
   qqq login -u atwalsh -t TOKEN
   ```

2. Change directories to the git repository you want to share
3. Checkout the branch you want to share
4. Run `qqq share` to make a new private repository on GitHub:
   ```bash
   # Share the currently checked out branch with 
   # GitHub user `atwalsh`
   
   qqq share atwalsh
   ``` 
   
### Options
#### `share`
- `-a` Adds an additional admin collaborator to the GitHub repository
  - Send multiple `-a` options to add multiple admin collaborators:
    ```bash
    # Send branch to `atwalsh`, add `MedShift` and `GridResearch` 
    # as admin collaborators
    
    qqq send atwalsh -a MedShift -a GridResearch
    ```