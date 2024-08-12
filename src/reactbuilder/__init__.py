import os, tempfile, shutil, subprocess
import hashlib
from typing import Union


def put_in_tempdir(react_dir: str, prev_tempdir: Union[str, None]=None, delete_existing: bool=True) -> str:
    """Given a react_dir (contains package.json), copy to a temporary dir for building."""
    
    src_hash = hashlib.md5(os.path.dirname(react_dir).encode()).hexdigest()  # consistent-length temp dir
    if prev_tempdir or prev_tempdir is None:
        # TODO: Use config for this.
        if prev_tempdir is None:
            import platform
            if platform.system() in ('Linux', 'FreeBSD', 'Darwin'):
                DEFAULT_TEMPDIR = f'/tmp/{src_hash}'
            elif platform.system() == 'Windows':
                DEFAULT_TEMPDIR = f'C:\\temp\\{src_hash}'
            else:
                raise Exception(f"Unsupported platform: {platform.system()}")
            prev_tempdir = os.environ.get('REACTBUILD_TEMPDIR', DEFAULT_TEMPDIR)
        temp_dir = prev_tempdir
    else:
        temp_dir = tempfile.mkdtemp()
    # Does the temp dir exist?
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Copy the react folder to a temp dir.
    shutil.copytree(react_dir, temp_dir, dirs_exist_ok=True) # dirs_exist_ok requires Python >=3.8

    # Make sure to delete package-lock.json and node_modules under the temp dir.
    if delete_existing:
        if os.path.exists(os.path.join(temp_dir, 'package-lock.json')):
            print('Deleting package-lock.json')
            os.remove(os.path.join(temp_dir, 'package-lock.json'))
        if os.path.exists(os.path.join(temp_dir, 'node_modules')):
            print('Deleting node_modules')
            shutil.rmtree(os.path.join(temp_dir, 'node_modules'), ignore_errors=True)
    
    return temp_dir


def get_npm_path_winps():
    # Run the PowerShell command and capture the output
    output = subprocess.check_output(
        'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -Command "Get-Command npm | Select-Object -ExpandProperty Source"',
        shell=True
    )
    # Decode the output from bytes to string and strip any extra whitespace
    npm_path = output.decode().strip()
    return npm_path


def build_site(temp_dir: str, do_install: bool=True) -> str:
    """Build the site in the temp dir."""
    os.chdir(temp_dir)
    if do_install:
        try:
            install_result = subprocess.run(['npm', 'install'])
        except FileNotFoundError:
            npmpath = get_npm_path_winps()
            install_result = subprocess.run([npmpath, 'install'])
        if install_result.returncode != 0:
            raise Exception('npm install failed')
        else:
            print('npm install successful')
    
    try:
        build_result = subprocess.run(['npm', 'run', 'build'])
    except FileNotFoundError:
        npmpath = get_npm_path_winps()
        build_result = subprocess.run([npmpath, 'run', 'build'])
    if build_result.returncode != 0:
        raise Exception('npm run build failed')
    else:
        print('npm run build successful')

    return build_result

def collect_artifacts(temp_dir: str, build_parent: str) -> str:
    # Copy the build folder back to here.
    build_dir = os.path.join(temp_dir, 'build')
    dest = os.path.join(build_parent, 'build')
    # Resolve all the .. etc to a simpler path:
    dest = os.path.normpath(dest)
    shutil.copytree(build_dir, dest, dirs_exist_ok=True)

    print(f'Site built successfully and copied to {dest}.')
    return dest
