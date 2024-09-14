#!/usr/bin/env python3

# Released under the Unlicense [https://github.com/JonTheNiceGuy/python_shell_script_template/blob/main/LICENSE] on 2024-09-14

# I'm under no obligation to fix anything here or maintain this at all! Feel free to reuse any components
# of this in your own work without assigning any credit. But, if you want to credit this git repo:
#   https://github.com/JonTheNiceGuy/python_shell_script_template
# or the related blog post
#   https://jon.sprig.gs/blog/post/8025
# that would be lovely!

import os
import logging
import argparse
import subprocess


class Colours:
    # Implementation based on ideas from https://stackoverflow.com/q/287871
    RESET = '\033[m'
    BOLD = '\033[1m'
  
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'

    BOLD_RED = '\033[31m\033[m'
    BOLD_GREEN = '\033[32m\033[m'
    BOLD_YELLOW = '\033[33m\033[m'
    BOLD_BLUE = '\033[34m\033[m'
    BOLD_PURPLE = '\033[35m\033[m'
    BOLD_CYAN = '\033[36m\033[m'

    def __init__(self, nocolour: bool = False):
        self.nocolour(nocolour)

    def nocolour(self, nocolour: bool = False):
        if (
            os.environ.get('NOCOLOUR', '') != '' or
            os.environ.get('NOCOLOR', '') != '' or
            nocolour
        ):
            self.RESET = ''
            self.BOLD = ''
          
            self.RED = ''
            self.GREEN = ''
            self.YELLOW = ''
            self.BLUE = ''
            self.PURPLE = ''
            self.CYAN = ''

            self.BOLD_RED = ''
            self.BOLD_GREEN = ''
            self.BOLD_YELLOW = ''
            self.BOLD_BLUE = ''
            self.BOLD_PURPLE = ''
            self.BOLD_CYAN = ''


class RunCommand:
    command = ''
    cwd = ''
    running_env = {}
    stdout = []
    stderr = []
    exit_code = 999

    def __init__(
        self,
        command: list = [],
        cwd: str = None,
        env: dict = None,
        raise_on_error: bool = True
    ):
        self.command = command
        self.cwd = cwd

        self.running_env = os.environ.copy()

        if env is not None and len(env) > 0:
            for env_item in env.keys():
                self.running_env[env_item] = env[env_item]

        logger.debug(f'exec: {" ".join(command)}')

        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
                env=self.running_env
            )
            # Store the result because it worked just fine!
            self.exit_code = 0
            self.stdout = result.stdout.splitlines()
            self.stderr = result.stderr.splitlines()
        except subprocess.CalledProcessError as e:
            # Or store the result from the exception(!)
            self.exit_code = e.returncode
            self.stdout = e.stdout.splitlines()
            self.stderr = e.stderr.splitlines()

        # If verbose mode is on, output the results and errors from the command execution
        if len(self.stdout) > 0:
            logger.debug(
                f'{colours.BOLD_GREEN}stdout:{colours.RESET}{colours.GREEN} {self.list_to_newline_string(self.stdout)}{colours.RESET}'
            )
        if len(self.stderr) > 0:
            logger.debug(
                f'{colours.BOLD_RED}stderr:{colours.RESET}{colours.RED} {self.list_to_newline_string(self.stderr)}{colours.RESET}'
            )

        # If it failed and we want to raise an exception on failure, record the command and args
        # then Raise Away!
        if raise_on_error and self.exit_code > 0:
            command_string = None
            args = []
            for element in command:
                if not command_string:
                    command_string = element
                else:
                    args.append(element)

            raise Exception(
                f'Error ({self.exit_code}) running command {command_string} with arguments {args}\nstderr: {self.stderr}\nstdout: {self.stdout}'
            )

    def __repr__(self) -> str:
        return "\n".join(
            [
               f"Command: {self.command}",
               f"Directory: {self.cwd if not None else '{current directory}'}",
               f"Env: {self.running_env}",
               f"Exit Code: {self.exit_code}",
               f"nstdout: {self.stdout}",
               f"stderr: {self.stderr}" 
            ]
        )

    def list_to_newline_string(self, list_of_messages: list):
        return "\n".join(list_of_messages)


# Set defaults here
logger = logging
colours = Colours()
# Main processes here


def main():
    args = process_args()

    print(f'Hello {args.who}')

    get_date = RunCommand(['date'])

    print("\n".join(get_date.stdout))

# Functions to support main()


def process_args():
    parser = argparse.ArgumentParser(
        description="A script to say hello world"
    )

    parser.add_argument(
        '--verbose', '-v',
        action="store_true",
        help="Be more verbose in logging [default: off]"
    )

    parser.add_argument(
        '--nocolour', '--nocolor',
        action="store_true",
        help="Be more verbose in logging [default: off]"
    )

    parser.add_argument(
        'who',
        help="The target of this script"
    )

    args = parser.parse_args()

    if args.verbose:
        logger.basicConfig(level=logging.DEBUG)
        logger.debug('Setting verbose mode on')
    else:
        logger.basicConfig(level=logging.INFO)

    colours.nocolour(args.nocolour)

    return args


# Run the main() function
if __name__ == "__main__":
    main()
