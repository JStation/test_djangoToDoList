from os import path
import subprocess
THIS_FOLDER = path.dirname(path.abspath(__file__))
FAB_PATH = path.abspath('C:\Python27\Scripts')
FAB_CMD = path.join(FAB_PATH, 'fab.exe')

def create_session_on_server(host, email):
    return subprocess.check_output(
        [
            FAB_CMD,
            'create_session_on_server:email={}'.format(email),
            '--host={}'.format(host),
            '--hide=everything,status',
        ],
        cwd=THIS_FOLDER
    ).decode().strip()

def reset_database(host):
    subprocess.check_call(
        [FAB_CMD, 'reset_database', '--host={}'.format(host)],
        cwd=THIS_FOLDER
    )