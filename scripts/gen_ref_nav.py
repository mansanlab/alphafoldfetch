"""Generate MkDocs reference pages for the local package."""

from pathlib import Path

import mkdocs_gen_files

for path in sorted(Path('affetch').rglob('*.py')):
    module_path = path.with_suffix('')
    doc_path = path.with_suffix('.md')
    full_doc_path = Path('reference', doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == '__init__':
        parts = parts[:-1]
        doc_path = doc_path.with_name('index.md')
        full_doc_path = full_doc_path.with_name('index.md')
    elif parts[-1] == '__main__':
        continue
    elif parts[-1] == '__version__':
        continue

    with mkdocs_gen_files.open(full_doc_path, 'w') as fd:
        fd.write(f"::: {'.'.join(parts)}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)
