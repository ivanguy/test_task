import os
import sys
import argparse
import importlib
import subprocess
from typing import List


def get_py_files(folder: str) -> List[str]:
    """
    Traverses folder returns files ending with '.py' sorted alphabetically
    """
    py_files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.py'):
                py_files.append(os.path.join(dirpath, filename))
    return sorted(py_files)


def name_from_path(path: str) -> str:
    """
    /path/to/file.py -> path_to_file
    """
    return "_".join(path.removesuffix('.py').split('/'))


def import_and_get_CMDS(path: str):
    """
    import module at path and return CMDS variable from that module
    """
    m_name = name_from_path(path)
    spec = importlib.util.spec_from_file_location(m_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[m_name] = module
    spec.loader.exec_module(module)
    return module.CMDS


if __name__ == "__main__":
    parser = argparse.ArgumentParser("CMDS runner")
    parser.add_argument("path", help="Path to directory containing CMDS")
    args = parser.parse_args()
    folder = args.path

    py_files = get_py_files(folder)
    commands_executed = set()
    for filepath in py_files:
        CMDS = import_and_get_CMDS(filepath)
        for cmd in CMDS:
            if cmd in commands_executed:
                print(f'команда {cmd} уже выполнялась')
                continue
            commands_executed.add(cmd)
            subprocess.run(cmd, shell=True)

