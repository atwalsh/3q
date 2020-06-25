import configparser
import os
import secrets
from pathlib import Path

import click
import click_spinner
import shortuuid
from git import Repo

from .github import GitHub

CONFIG_FILE = 'config.ini'
QQQ = 'qqq'


@click.group()
def cli():
    pass


@cli.command()
@click.option('-u', '--user', 'user')
@click.option('-t', '--token', 'token')
def login(user, token):
    app_dir = click.get_app_dir(QQQ)
    config_path = f'{app_dir}/{CONFIG_FILE}'

    # Verify user
    with click_spinner.spinner():
        if not GitHub.verify_token(user, token):
            click.echo(click.style('Invalid GitHub username or token!', fg='red'))
            raise click.Abort

    # Check if file already exists
    if Path(config_path).is_file():
        # File exists, prompt to overwrite
        click.confirm(f'{click.format_filename(config_path)} already exists, update?', abort=True)

    # Create config object
    cp = configparser.ConfigParser()
    cp['auth'] = {
        'user': user,
        'token': token
    }

    # Make sure the qqq dir exists
    if not Path(app_dir).is_dir():
        click.echo(f'Creating directory {click.format_filename(app_dir)}...')
        Path(app_dir).mkdir(parents=True, exist_ok=True)

    # Write to config file
    with open(config_path, 'w') as config_file:
        cp.write(config_file)
        click.echo(f'Updated config file located at:\t{click.format_filename(config_path)}')


@cli.command()
@click.argument('github_username')
@click.option('-a', '--admins', multiple=True, required=False)
def send(github_username, admins):
    config_path = f'{click.get_app_dir(QQQ)}/{CONFIG_FILE}'
    # Make sure config file exists
    if not Path(config_path).is_file():
        click.echo(click.style('Config files does not exist. Run `qqq login`.', fg='red'))
        raise click.Abort

    # Read the config file
    cp = configparser.ConfigParser()
    try:
        cp.read(config_path)
        auth_user = cp.get('auth', 'user')
        auth_token = cp.get('auth', 'token')
    except configparser.Error:
        click.echo(click.style('Malformed configuration file.', fg='red'))
        raise click.Abort
    gh = GitHub(auth_user, auth_token)
    # Verify user exists on GitHub
    user = gh.get_user(github_username)
    if user is None:
        click.echo(f'Could not find GitHub user {github_username}.')
        raise click.Abort

    # Create the repo object
    repo = Repo(os.getcwd())
    if repo.bare:
        # Confirm the user wants to use an empty repo
        click.confirm('Repository appears to be bare, continue?', abort=True)

    # Generate new repo name
    repo_name = f'{github_username}-{shortuuid.uuid()}'
    # Ask user for branch name
    branch_name = click.prompt('Enter the branch name on the remote repository', default='master')

    # Confirm with user
    click.echo(f'Preparing to send the current branch to {github_username}...')
    _repo = f''
    _msg = f'''Are you sure you want to send the current branch to {user["login"]} ({user["name"]})? This will:
    \t1. Take the current `{repo.active_branch}` branch and force push to {auth_user}/{repo_name} on GitHub (private)
    \t2. Invite {github_username} as a collaborator\n'''
    if admins:
        _msg += f'\t3. Invite {", ".join([str(a) for a in admins])} as {"an " if len(admins) == 1 else ""}' \
                f'admin collaborator{"s" if len(admins) > 1 else ""}\n'
    click.confirm(click.style(_msg, fg='cyan'), abort=True)

    click.echo(f'Creating repo on GitHub and inviting {user["login"]}...')
    with click_spinner.spinner():
        # Create repo on GitHub
        new_repo = gh.create_repo(repo_name)
        if new_repo is None:
            click.echo(click.style('Failed to create repository on GitHub.', fg='red'))
            raise click.Abort

        # Push the current branch to the new repo
        _tmp_remote_name = secrets.token_urlsafe()
        _tmp_remote_url = f'https://{auth_token}:x-oauth-basic@github.com/{auth_user}/{repo_name}.git'
        new_remote = repo.create_remote(_tmp_remote_name, _tmp_remote_url)
        new_remote.push(f'{repo.head.ref}:{branch_name}')
        repo.delete_remote(_tmp_remote_name)
        if not gh.add_collaborator(repo_name, user["login"]):
            click.echo(click.style(f'Error inviting {user["login"]}.', fg='red'))

    # Invite admin collaborators
    for admin_username in admins:
        au = gh.get_user(admin_username)  # Verify the admin collaborator's GitHub account
        if au:
            click.confirm(click.style(f'Are you sure you want to invite {au["login"]} as an admin?', fg='cyan'))
            click.echo(f'Inviting admin {au["login"]} ({au["name"]})...')
            with click_spinner.spinner():
                if not gh.add_collaborator(repo_name, admin_username, admin=True):
                    click.echo(click.style(f'Error inviting {au["login"]}.', fg='red'))
        else:
            click.echo(click.style(f'Could not find {admin_username}.', fg='red'))
    click.echo('Done!')
