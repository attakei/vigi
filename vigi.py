#!/usr/bin/env python
import subprocess
from pathlib import Path
from subprocess import CalledProcessError, PIPE
from textwrap import dedent


__version__ = '0.1.0'


gi_line_custom = "# ~~~ Write your custom ignore target ~~~"
gi_line_online = "# ~~~ Write your gitignore envs ~~~"

gi_template = f"""
    {gi_line_custom}

    {gi_line_online}
"""


def main():
    gi_path = Path.cwd() / '.gi'
    gitignore_path = Path.cwd() / '.gitignore'
    try:
        # Convert from ``.gitignore`` to ``.gi``
        if gitignore_path.exists():
            pass
        else:
            with gi_path.open('w') as fp:
                fp.write(dedent(gi_template).strip())
        # Spawn vim
        vim_args = ['/usr/bin/vim', str(gi_path)]
        vim_proc = subprocess.run(vim_args, check=True)
        # Convert from ``.gi`` to ``.gitignore``
    except CalledProccessError:
        pass
    finally:
        # Remove ``.gi``
        gi_path.unlink()


if __name__ == '__main__':
    main()
