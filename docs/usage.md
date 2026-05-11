# Usage

```bash
affetch [OPTIONS] UNIPROT...
```

`UNIPROT...` can be UniProt accessions, FASTA files, strings containing UniProt accessions, or `-` for stdin.

## Options

| Option | Default | Description |
| --- | --- | --- |
| `--output`, `-o` | `.` | Existing directory where files are saved |
| `--file-type`, `-f` | `pcz` | Output selector: `p` for PDB, `c` for CIF, `z` for gzip |
| `--model`, `-m` | `6` | AlphaFold model version, `1` through `6` |
| `--n-sync` | `50` | Concurrent download requests |
| `--n-save` | `500` | File writes submitted per batch |

Run `affetch --help` for the full Typer-generated help output.

## Inputs

AlphaFoldFetch accepts:

- UniProt accessions like `P11388`
- strings that contain a valid UniProt accession
- FASTA files ending in `.fasta`, `.fas`, `.fa`, or `.faa`
- `-` to read whitespace-separated input from stdin

FASTA parsing only scans header lines and keeps validated UniProt accessions.

## Outputs

The `--file-type` option combines three letters:

- `p`: save PDB files
- `c`: save CIF files
- `z`: gzip the selected files

The default `pcz` downloads gzipped PDB and CIF files:

```text
AF-P11388-F1-model_v6.pdb.gz
AF-P11388-F1-model_v6.cif.gz
```

Common file-type choices:

| Value | Result |
| --- | --- |
| `p` | Uncompressed PDB only |
| `c` | Uncompressed CIF only |
| `pc` | Uncompressed PDB and CIF |
| `pz` | Gzipped PDB only |
| `cz` | Gzipped CIF only |
| `pcz` | Gzipped PDB and CIF |

The output directory must already exist. Accessions without an available AlphaFold file are skipped.

## Examples

Download one accession:

```bash
affetch P11388
```

Download several accessions:

```bash
affetch P11388 Q01320 P41516
```

Save into an existing directory:

```bash
mkdir -p structures
affetch -o structures P11388
```

Download an uncompressed PDB only:

```bash
affetch -f p P11388
```

Use a specific AlphaFold model version:

```bash
affetch --model 5 P11388
```

Download structures from FASTA files:

```bash
affetch UP000005640_9606.fasta
affetch plant_pgks.fasta mammalian_pgks.fasta bacterial_pgks.fasta
```

Read accessions from stdin:

```bash
printf "P11388\nQ01320\n" | affetch -
```

From an AlphaFold DB search results CSV:

```bash
tail -n +2 results-csv.csv | while IFS='-' read -r f1 f2 f3; do echo $f2; done | affetch -
```

From [getSequence](https://github.com/alexholehouse/getSequence):

```bash
getseq human top2a, mouse top2a, rat top2a | affetch -
```
