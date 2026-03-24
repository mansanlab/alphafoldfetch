# AlphaFoldFetch

AlphaFoldFetch is a command-line tool for downloading AlphaFold structure files from UniProt IDs and UniProt FASTA files.

It is meant for fast batch workflows:

- download one or many structure in one command
- choose any combination of PDB, CIF, or gzipped outputs
- tune concurrency for larger downloads

## CLI Summary

```bash
affetch [OPTIONS] UNIPROT...
```

Arguments:

- `UNIPROT...`: UniProt IDs, FASTA files, or `-` for stdin

Options:

- `--output`, `-o`: output directory
- `--file-type`, `-f`: any combination of `p`, `c`, and `z`
- `--model`, `-m`: AlphaFold model version `1` through `6`
- `--n-sync`: concurrent download requests
- `--n-save`: file writes submitted per batch

## Input Rules

AlphaFoldFetch accepts:

- raw UniProt accessions like `P11388`
- text that contains a valid UniProt accession
- FASTA files ending in `.fasta`, `.fas`, `.fa`, or `.faa`
- `-` to read whitespace-separated input from stdin

FASTA parsing only keeps validated UniProt IDs from header lines.

## Output Rules

The default file-type value is `pcz`, which means:

- `p`: PDB output
- `c`: CIF output
- `z`: gzip compression

So the default behavior downloads both PDB and CIF files as gzip outputs.

## Examples

Single AlphaFold structure

```bash
affetch P11388
```

Multiple AlphaFold structures

```bash
affetch P11388 Q01320 P41516
```

Structures from a single UniProt FASTA file

```bash
affetch UP000005640_9606.fasta
```

Multiple UniProt FASTA files

```bash
affetch UP000007305_4577.fasta UP000005640_9606.fasta UP000000625_83333.fasta
```
*First obtain these FASTA files from UniProt*

Multiple custom FASTA files

```bash
affetch plant_pgks.fasta mammalian_pgks.fasta bacterial_pgks.fasta
```
*Input files must be in the UniProt FASTA file format*

Unzipped PDB file

```bash
affetch -f p P11388
```
*Default will dowload zipped PDB and CIF files for all entries*

Redirect output to a directory

```bash
mkdir human_top2a && affetch -o ./human_top2a P11388
```

EBI AlphaFold Download data - Search Results CSV File

```bash
tail -n +2 results-csv.csv | while IFS='-' read -r f1 f2 f3; do echo $f2; done | affetch -
```

Don't know the UniProt ID? Use [getSequence](https://github.com/alexholehouse/getSequence) and pipe into `affetch`

```bash
getseq human top2a, mouse top2a, rat top2a | affetch -
```
*Pipe input arguments must be indicated with a dash `-`*
