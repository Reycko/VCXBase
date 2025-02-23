"""Setup"""
from dataclasses import dataclass
import os
import re
import shutil
import subprocess
import sys
import argparse
import uuid

INTERACTIVE: bool = len(sys.argv) < 2

@dataclass
class Options:
    """Project options"""
    name: str = 'Project'
    uuid: str = 'auto'
    origin: str = ''
    delete: bool = False

DRY = False
SCRIPT_DIR: str =  os.path.dirname(os.path.realpath(__file__))

UUID_REGEX = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
                        re.IGNORECASE)

EXTRACT_INFO_FROM_SOLUTION = re.compile(
    r'^Project\("\{(?:.*)\s*=\s*"(.*?)",\s*"(.*?)",\s*"\{(.*)\}"$', re.MULTILINE)

OPTS: Options = Options()

def parse_args() -> None:
    """Parses arguments with argparse"""
    parser = argparse.ArgumentParser('VCXBase Setup')
    parser.add_argument('-n', '--name', dest='name', required=False, default=Options.name)
    parser.add_argument('-u', '--uuid', dest='uuid', required=False, default=Options.uuid)
    parser.add_argument('-o', '--origin', dest='origin', required=False, default='')
    parser.add_argument('-a', '--auto', dest='auto', required=False, default=False,
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('-D', '--delete-self', dest='delete', required=False, default=False,
                        action=argparse.BooleanOptionalAction)

    parsed = parser.parse_args()

    if parsed.auto:
        OPTS.name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        OPTS.uuid = 'auto'
    else:
        OPTS.name = parsed.name if parsed.name else Options.name
        OPTS.uuid = parsed.uuid.lower() if parsed.uuid else Options.uuid
    OPTS.delete = parsed.delete if parsed.delete else Options.delete
    OPTS.origin = parsed.origin if parsed.origin else Options.origin


def interactive() -> None:
    """Interactive mode"""
    while True:
        name = input('Project name: ')
        if (len(name) > 0 and name.isalnum()):
            OPTS.name = name
            break

        print('Must be an alphanumeric string with at least 1 character.')
    while True:
        input_uuid = input('Project UUID (auto = generates one for you): ').lower()
        if bool(UUID_REGEX.match(input_uuid)) or input_uuid == 'auto':
            OPTS.uuid = input_uuid
            break

        print('Invalid UUID.')

    OPTS.origin = input('Set git origin? Leave blank to not set: ')
    OPTS.delete = input('Do you want the script to delete itself once it is done running? [Y/n]: ').lower() == 'n'

    OPTS.name = ''.join(c for c in OPTS.name if c.isalnum())
    print('Project name: ' + OPTS.name)
    print('Project UUID: ' + '(generate one for me)' if OPTS.uuid == 'auto' else OPTS.uuid)
    print('Set origin to: ' + '(none)' if OPTS.origin == '' else OPTS.origin)
    print('Self-Destruct after launch: ' + 'Yes' if OPTS.delete else 'No')

    if INTERACTIVE:
        print('Is this correct?')
        correct = input('[Y/n] ')
        if correct.lower() == 'n':
            interactive()

def make_project_path(name: str) -> str:
    """Returns the VC++ project path from the name"""
    return name + os.path.sep + name + '.vcxproj'

def rename(src: str, dst: str, rel: str | None = None):
    """Calls os.rename if not dry"""
    if not DRY:
        os.rename(src, dst)
    prefix = 'file' if os.path.isfile(src) else 'folder'
    src_rel = os.path.relpath(src, rel) if rel else os.path.abspath(src)
    dst_rel = os.path.relpath(dst, rel) if rel else os.path.abspath(dst)
    print(f'Renamed {prefix} {src_rel} to {dst_rel}')

def main() -> int:
    """Main"""
    if os.name != 'nt':
        print('This script only runs in Windows.')
        return 1

    if INTERACTIVE:
        print('Launching interactive mode as no arguments were provided.')
        interactive()
    else:
        parse_args()

    print('Project name: ' + OPTS.name)
    print('Project UUID: ' + '(generate one for me)' if OPTS.uuid == 'auto' else OPTS.uuid)
    print('Set origin to: ' + '(none)' if OPTS.origin == '' else OPTS.origin)
    print('Self-Destruct after launch: ' + 'Yes' if OPTS.delete else 'No')

    OPTS.name = ''.join(c for c in OPTS.name if c.isalnum())

    if OPTS.uuid == 'auto':
        OPTS.uuid = str(uuid.uuid4())

    sln_path = ''
    base_name = ''
    base_proj_path = ''
    base_uuid = ''
    for n in os.listdir(SCRIPT_DIR):
        sln_path = os.path.join(SCRIPT_DIR, n)
        if n.lower().endswith('.sln'):
            print('Found solution ' + n)
            data = ''
            with open(sln_path, 'r', encoding='utf-8') as f:
                data = f.read()
            matches = EXTRACT_INFO_FROM_SOLUTION.search(data)
            if matches:
                base_name = str(matches[1])
                base_proj_path = str(matches[2])
                base_uuid = str(matches[3])
                data: str = data.replace(base_name, OPTS.name)
                data = data.replace(base_proj_path, make_project_path(OPTS.name))
                data = data.replace(base_uuid, OPTS.uuid.upper())
                if not DRY:
                    with open(sln_path, 'w', encoding='utf-8') as f:
                        f.write(data)
                        f.flush()
                print('Updated name, UUID, and vcxproj path for ' + base_name)
                print('\tOld UUID: ' + base_uuid)
                print('\tNew UUID: ' + OPTS.uuid.upper())
                print('\t' + ('-' * 8))
                print('\tOld Name: ' + base_name)
                print('\tNew Name: ' + OPTS.name)

    if base_name + base_proj_path + base_uuid == '':
        print('Could not find a solution to extract values from, or solution was invalid.')
        return 1

    if not os.path.exists(os.path.join(SCRIPT_DIR, base_proj_path)):
        print('Could not find .vcxproj file.')
        return 1

    with open(os.path.join(SCRIPT_DIR, base_proj_path), 'r+', encoding='utf-8') as f:
        data: str = f.read()
        data = data.replace(base_name, OPTS.name)
        data = data.replace(base_uuid, OPTS.uuid)

        if not DRY:
            f.seek(0)
            f.write(data)
            f.truncate()
        print('Updated name and UUID for ' + base_proj_path)

    rename(sln_path, os.path.join(SCRIPT_DIR, OPTS.name + '.sln'), SCRIPT_DIR)

    proj_folder: str = os.path.dirname(os.path.join(SCRIPT_DIR, base_proj_path))
    for f in os.listdir(proj_folder):
        full: str = os.path.join(proj_folder, f)
        if f.startswith(os.path.basename(base_proj_path)) and os.path.isfile(full):
            suffix = f.replace(os.path.basename(base_proj_path), '', 1)
            new_path = os.path.join(proj_folder, os.path.basename(base_proj_path).replace(base_name, OPTS.name, 1) + suffix) # pylint: disable=line-too-long
            rename(full, new_path, SCRIPT_DIR)

    rename(os.path.dirname(os.path.join(SCRIPT_DIR, base_proj_path)),
           os.path.join(SCRIPT_DIR, OPTS.name),
           SCRIPT_DIR)

    if not DRY:
        if shutil.which('git') is not None:
            # TODO: maybe some error handling here?
            subprocess.run(f'cmd /c del /f /s /q "{os.path.join(SCRIPT_DIR, '.git')}"',
                           stdout=subprocess.DEVNULL, check=True, shell=True)

            git_config = subprocess.run(['git', 'config', '--global', '--list'],
                                        stdout=subprocess.PIPE, text=True, check=True).stdout

            os.system('git init -b master')

            was_gpg = False
            if 'commit.gpgsign=true' in git_config:
                was_gpg = True
                print('Found commit.gpgsign to be true. This will be set to false temporarily.')
                os.system('git config --global commit.gpgsign false')
            os.system('git add .')
            os.system('git rm --cached ./LICENSE')
            os.system('git rm --cached ./README.md')
            os.system('git commit -m "feat: initial commit"')
            os.system('git branch develop')
            if len(OPTS.origin) > 0:
                os.system('git remote add origin ' + OPTS.origin)
            if was_gpg:
                os.system('git config --global commit.gpgsign true')
        else:
            print('Git is not installed. You will have to make the repository yourself.')

        print('\nFinished Git setup. Modify the README.md and LICENSE if you want to, they have not been commited yet.') # pylint: disable=line-too-long
        if OPTS.delete:
            os.remove(__file__)
    return 0

if __name__ == '__main__':
    sys.exit(main())
