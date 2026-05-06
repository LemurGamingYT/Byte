from pathlib import Path
from json import dumps

from byte import ast


def create_new_project(name: str, path: Path):
    src_folder = path / 'src'
    src_folder.mkdir()

    main_file = src_folder / 'main.byte'
    main_file.write_text("""fn main() -> int {
    // write code here
    return 0
}
""")
    
    project_info = {
        'name': name,
        'version': '0.1',
        'byte-version': ast.VERSION,
        'entry': str(main_file.relative_to(path))
    }

    project_json = path / 'project.json'
    project_json.write_text(dumps(project_info, indent=4))
