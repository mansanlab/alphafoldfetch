![AlphaFoldFetch logo](docs/assets/images/affetch_logo.png)

# AlphaFoldFetch

AlphaFoldFetch is a small command-line tool for downloading AlphaFold structure files from UniProt accessions or UniProt-style FASTA files.

It is built for quick one-off downloads and simple batch workflows:

- pass one ID, many IDs, FASTA files, or stdin
- download PDB, CIF, or both
- optionally gzip the saved files
- tune concurrency for larger jobs

## Benchmark

Local benchmark against the AlphaFold *Homo sapiens* proteome with 47,172 gzipped structures (pdb + cif).

![benchmark](docs/assets/images/benchmark.png)


## Install

Run once with `uvx`:

```bash
uvx --from AlphaFoldFetch affetch P11388
```

Or install the `affetch` command:

```bash
uv tool install AlphaFoldFetch
```

AlphaFoldFetch requires Python 3.11 or newer.

## Quick Start

Download the default outputs for one UniProt accession:

```bash
affetch P11388
```

Download several accessions:

```bash
affetch P11388 Q01320 P41516
```

Write files to an existing directory:

```bash
mkdir -p structures
affetch -o structures P11388
```

Download an uncompressed PDB only:

```bash
affetch -f p P11388
```

Read IDs from stdin:

```bash
printf "P11388\nQ01320\n" | affetch -
```

## Usage

```bash
affetch [OPTIONS] UNIPROT...
```

Arguments:

- `UNIPROT...`: UniProt IDs, FASTA files, or `-` for stdin

Common options:

- `--output`, `-o`: output directory, default: current directory
- `--file-type`, `-f`: any combination of `p`, `c`, and `z`, default: `pcz`
- `--model`, `-m`: AlphaFold model version, default: `6`
- `--n-sync`: concurrent download requests, default: `50`
- `--n-save`: file writes submitted per batch, default: `500`

## Input Rules

AlphaFoldFetch accepts:

- UniProt accessions like `P11388`
- strings that contain a valid UniProt accession
- FASTA files ending in `.fasta`, `.fas`, `.fa`, or `.faa`
- `-` to read whitespace-separated input from stdin

FASTA parsing only keeps validated UniProt IDs from header lines.

## Output Rules

The `--file-type` option is a compact set of letters:

- `p`: save PDB files
- `c`: save CIF files
- `z`: gzip the selected outputs

The default value is `pcz`, so `affetch P11388` downloads gzipped PDB and CIF files for AlphaFold model 6:

```text
AF-P11388-F1-model_v6.pdb.gz
AF-P11388-F1-model_v6.cif.gz
```

Examples:

- `-f p`: uncompressed PDB only
- `-f c`: uncompressed CIF only
- `-f pc`: uncompressed PDB and CIF
- `-f pz`: gzipped PDB only
- `-f cz`: gzipped CIF only

The output directory must already exist. IDs without an available AlphaFold file are skipped.

## FASTA Files

Download structures from one or more UniProt FASTA files:

```bash
affetch UP000005640_9606.fasta
affetch plant_pgks.fasta mammalian_pgks.fasta bacterial_pgks.fasta
```

Only header lines are scanned for UniProt accessions.

## Pipelines

From an AlphaFold DB search results CSV:

```bash
tail -n +2 results-csv.csv | while IFS='-' read -r f1 f2 f3; do echo $f2; done | affetch -
```

From [getSequence](https://github.com/alexholehouse/getSequence):

```bash
getseq human top2a, mouse top2a, rat top2a | affetch -
```

Remember to pass `-` when reading IDs from stdin.

## More Information

- Documentation: <https://mansanlab.github.io/alphafoldfetch/>
- Issues: <https://github.com/mansanlab/alphafoldfetch/issues>

## Credits

Inspired by [getSequence](https://github.com/alexholehouse/getSequence).
