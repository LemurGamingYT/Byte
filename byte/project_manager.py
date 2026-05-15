from json import dumps, loads
from pathlib import Path

from byte.ast import VERSION as BYTE_VERSION


def create_project(project_folder: Path, project_name: str):
    src_folder = project_folder / 'src'
    src_folder.mkdir()

    main_file = src_folder / 'main.byte'
    main_file.write_text("""fn main() -> int {
    print("Hello, World!")
    return 0
}
""")

    config = {
        'name': project_name,
        'version': '0.1',
        'byte-version': BYTE_VERSION,
        'entry': str(main_file.relative_to(project_folder)),
        'directory': str(project_folder)
    }

    config_json = project_folder / 'config.json'
    config_json.write_text(dumps(config, indent=4))

def get_entry_file(path: Path):
    config_json = path / 'config.json'
    if not config_json.is_file():
        return False, 'directory does not contain a config.json file or it is not a file'

    config = loads(config_json.read_text())
    if config.get('entry') is None:
        return False, 'config.json file does not contain an entry point'

    entry = path / Path(config['entry'])
    if not entry.is_file():
        return False, 'config.json contains an entry point file but it does not exist or it is not a file'

    return True, entry
