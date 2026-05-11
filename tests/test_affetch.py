import gzip

import pytest
from typer.testing import CliRunner

import affetch
from affetch.main import (
    alphafold_api_url,
    alphfold_file_url,
    app,
    chunk_urls,
    is_fasta_path,
    normalize_file_type,
    save_structures,
    validate_fasta,
    validate_uniprot_id,
    write_gz_structure,
    write_structure,
)

runner = CliRunner()


def test_validate_uniprot_id_accepts_known_id() -> None:
    assert validate_uniprot_id('P11388')


def test_validate_uniprot_id_rejects_invalid_id() -> None:
    assert not validate_uniprot_id('not-a-uniprot-id')


def test_package_version_is_available() -> None:
    assert affetch.__version__ == '1.0.2'


def test_chunk_urls_splits_values_by_size() -> None:
    chunks = list(chunk_urls(['a', 'b', 'c', 'd', 'e'], 2))
    assert chunks == [['a', 'b'], ['c', 'd'], ['e']]


def test_chunk_urls_accepts_iterables() -> None:
    chunks = list(chunk_urls((url for url in ['a', 'b', 'c']), 2))
    assert chunks == [['a', 'b'], ['c']]


def test_chunk_urls_rejects_non_positive_size() -> None:
    with pytest.raises(ValueError, match='at least 1'):
        list(chunk_urls(['a'], 0))


def test_alphafold_urls_match_expected_layout() -> None:
    assert alphafold_api_url('P11388').endswith('/P11388?key=AIzaSyCeurAJz7ZGjPQUtEaerUkBZ3TaBkXrY94')
    assert alphfold_file_url('P11388', 4, 'pdb').endswith('/AF-P11388-F1-model_v4.pdb')


def test_normalize_file_type_accepts_supported_letters() -> None:
    assert normalize_file_type('PCZ') == 'pcz'


def test_normalize_file_type_rejects_unsupported_letters() -> None:
    with pytest.raises(ValueError, match='unsupported option'):
        normalize_file_type('px')


def test_normalize_file_type_requires_structure_output() -> None:
    with pytest.raises(ValueError, match='must contain `p` and/or `c`'):
        normalize_file_type('z')


def test_is_fasta_path_is_case_insensitive() -> None:
    assert is_fasta_path('proteins.FASTA')
    assert not is_fasta_path('proteins.txt')


def test_validate_fasta_reads_valid_uniprot_headers(tmp_path) -> None:
    fasta = tmp_path / 'proteome.fasta'
    fasta.write_text('>sp|P11388|TOP2A_HUMAN DNA topoisomerase 2-alpha\nMADEUPSEQ\n', encoding='utf-8')

    assert validate_fasta(str(fasta)) == ['P11388']


def test_write_structure_writes_plain_text(tmp_path) -> None:
    output = tmp_path / 'AF-P11388-F1-model_v4.pdb'

    write_structure(output, 'structure-data')

    assert output.read_text(encoding='utf-8') == 'structure-data'


def test_write_gz_structure_writes_gzip_text(tmp_path) -> None:
    output = tmp_path / 'AF-P11388-F1-model_v4.cif'

    write_gz_structure(output, 'compressed-structure')

    with gzip.open(f'{output}.gz', 'rt', encoding='utf-8') as handle:
        assert handle.read() == 'compressed-structure'


def test_save_structures_surfaces_writer_errors(tmp_path) -> None:
    def failing_writer(file_path, structure):
        message = 'disk full'
        raise OSError(message)

    structures = {'https://alphafold.ebi.ac.uk/files/AF-P11388-F1-model_v4.pdb': 'structure-data'}

    with pytest.raises(OSError, match='disk full'):
        save_structures(tmp_path, structures, failing_writer)


def test_cli_rejects_zero_n_sync_before_download() -> None:
    result = runner.invoke(app, ['--n-sync', '0', 'P11388'])

    assert result.exit_code != 0
    assert '0' in result.output


def test_cli_rejects_file_output_path(tmp_path) -> None:
    output_file = tmp_path / 'not-a-directory'
    output_file.write_text('', encoding='utf-8')

    result = runner.invoke(app, ['--output', str(output_file), 'P11388'])

    assert result.exit_code != 0


def test_cli_reports_missing_uppercase_fasta_file() -> None:
    result = runner.invoke(app, ['missing.FASTA'])

    assert result.exit_code == 1
    assert 'Could not read FASTA file' in result.output
