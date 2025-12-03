import subprocess
import datetime
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true',
                    help='Use demo.txt instead of input.txt')
parser.add_argument('--verbose', action='store_true',
                    help='Enable verbose output')
args = parser.parse_args()

BASE_DIR = os.path.dirname(__file__)
CHALLENGES_DIR = os.path.join(BASE_DIR, 'challenges')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'monitor.log')

os.makedirs(LOG_DIR, exist_ok=True)


def run_and_log(script_path, log_handle):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    challenge_name = os.path.basename(os.path.dirname(script_path))
    try:
        cmd = ['python', script_path]
        if args.debug:
            cmd.append('--debug')
        if args.verbose:
            cmd.append('--verbose')

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=600)
        status = 'SUCCESS' if result.returncode == 0 else 'FAIL'
        output = result.stdout + '\n' + result.stderr
    except Exception as e:
        status = 'ERROR'
        output = str(e)
    log_handle.write(
        f'[{now}] [{status}] Output for {challenge_name}:\n{output}\n---\n')


def find_and_run_all_main_py():
    with open(LOG_FILE, 'w', encoding='utf-8') as log_handle:
        for entry in os.scandir(CHALLENGES_DIR):
            if entry.is_dir():
                main_py = os.path.join(entry.path, 'main.py')
                print(f'Running challenge in directory: {main_py}')
                if os.path.isfile(main_py):
                    run_and_log(main_py, log_handle)


if __name__ == '__main__':
    find_and_run_all_main_py()
