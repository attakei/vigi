#!/usr/bin/env python
import subprocess
from pathlib import Path
from subprocess import CalledProcessError, PIPE
from textwrap import dedent
from urllib.error import HTTPError
from urllib.request import urlopen, Request


__version__ = '0.1.0'


gi_line_custom = "# ~~~ Write your custom ignore target ~~~"
gi_line_online = "# ~~~ Write your gitignore envs ~~~"

gi_template = f"""
    {gi_line_custom}

    {gi_line_online}
"""


def decode_gitignore(src, dest):
    custom = []
    online = []
    with src.open() as fp:
        state = 'custom'
        for l in fp:
            line = l.strip()
            if line == gi_line_online:
                custom.append(line)
                state = 'online'
            elif state == 'custom':
                custom.append(line)
            else:
                online.append(line.lower())
    if online:
        url = f'https://www.gitignore.io/api/{",".join(online)}'
        req = Request(url, None, headers={'User-Agent': 'vigi'})
        try:
            resp = urlopen(req)
            custom.append(resp.read().decode())
        except HTTPError as err:
            if err.code == 404:
                custom.append(resp.read().decode())
            raise err
    with dest.open('w') as fp:
        fp.write('\n'.join(custom))


def encode_gitignore(src, dest):
    custom = []
    with src.open() as fp:
        state = 'custom'
        for l in fp:
            line = l.strip()
            if line == gi_line_online:
                custom.append(line)
                fp.readline()
                line = fp.readline().strip()
                envs = line.split('/')[-1]
                custom.append(envs)
                break
            elif state == 'custom':
                custom.append(line)
    with dest.open('w') as fp:
        fp.write('\n'.join(custom))


def main():
    gi_path = Path.cwd() / '.gi'
    gitignore_path = Path.cwd() / '.gitignore'
    try:
        # Convert from ``.gitignore`` to ``.gi``
        if gitignore_path.exists():
            encode_gitignore(gitignore_path, gi_path)
        else:
            with gi_path.open('w') as fp:
                fp.write(dedent(gi_template).strip())
        # Spawn vim
        vim_args = ['/usr/bin/vim', str(gi_path)]
        vim_proc = subprocess.run(vim_args, check=True)
        # Convert from ``.gi`` to ``.gitignore``
        decode_gitignore(gi_path, gitignore_path)
    except CalledProcessError:
        pass
    finally:
        # Remove ``.gi``
        gi_path.unlink()


if __name__ == '__main__':
    main()
