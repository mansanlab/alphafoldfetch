import gzip

from affetch.main import (
    alphafold_api_url,
    alphfold_file_url,
    chunk_urls,
    validate_fasta,
    validate_uniprot_id,
    write_gz_structure,
    write_structure,
)


def test_validate_uniprot_id_accepts_known_id() -> None:
    assert validate_uniprot_id('P11388')


def test_validate_uniprot_id_rejects_invalid_id() -> None:
    assert not validate_uniprot_id('not-a-uniprot-id')


def test_chunk_urls_splits_values_by_size() -> None:
    chunks = list(chunk_urls(['a', 'b', 'c', 'd', 'e'], 2))
    assert chunks == [['a', 'b'], ['c', 'd'], ['e']]


def test_alphafold_urls_match_expected_layout() -> None:
    assert alphafold_api_url('P11388').endswith('/P11388?key=AIzaSyCeurAJz7ZGjPQUtEaerUkBZ3TaBkXrY94')
    assert alphfold_file_url('P11388', 4, 'pdb').endswith('/AF-P11388-F1-model_v4.pdb')


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
