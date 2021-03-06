from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/JStation/test_djangoToDoList.git'

def deploy():
    site_folder = '/home/%s/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _update_wsgi_file(source_folder, site_folder)
    _reboot_python()

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source', 'public'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    # TODO: remove 'www.' prefix and correct settings in Dreamhost panel
    # correct setting should leave url alone rather than prepend 'www.'
    sed(settings_path, 'DOMAIN = "localhost"', 'DOMAIN = "%s"' % ('www.' + site_name,))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

    # set static directory for Passenger/Dreamhost compatibility
    sed(settings_path,
        "STATIC_ROOT = .+$",
        "STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, \"../public/static\"))"
        )

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder,
    ))

def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder
    ))

def _update_wsgi_file(source_folder, site_folder):
    deploy_tools_folder = source_folder + '/deploy_tools'
    wsgi_file = 'passenger_wsgi.py'
    run('cp %s/%s %s' % (
        deploy_tools_folder,
        wsgi_file,
        site_folder
    ))

def _reboot_python():
    run('pkill python')