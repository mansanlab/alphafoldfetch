[AlphaFoldFetch Dog](docs/assets/images/affetch_logo.png)

# AlphaFoldFetch

A tool for downloading AlphaFold structures using UniProt IDs or FASTA files

## What is AlphaFoldFetch?

AlphaFoldFetch is a command-line tool for downloading protein structural predictions from DeepMind's AlphaFold using UniProt IDs or FASTA files as input.

This tool is handy for getting structures for proteomes that are unavailable on AlphaFold's bulk download page.

### How does it work?

AlphaFoldFetch uses UniProt IDs and UniProt-formatted FASTA files to query AlphaFold's API and download structures within your terminal! You can specify the protein structure file type (PDB or CIF), whether your files are zipped or not (.gz), the AlphaFold model to access (v1–4), and download parameters to optimize large queries (>10,000 entries).

## Install

```bash
pip install alphafoldfetch
```

## Usage

```bash
affetch [OPTIONS] UNIPROT...
```

|Arguments  |Details                       |
|:----------|:-----------------------------|
|`UNIPROT`  |UniProt ID(s) or FASTA file(s)|

|Options            |Details                                          |
|:------------------|:------------------------------------------------|
|`--output`, `-o`   |Output directory                                 |
|`--file-type`, `-f`|File type(s), `p` = .pdb, `c` = .cif, `z` = *.gz |
|`--model`, `-m`    |AlphaFold model version, `1`, `2`, `3`, `4`      |
|`--n-sync`         |Syncronized number of downloads, Default = `50`  |
|`--n-save`         |Concurrent number of file writes, Default = `500`|

### Examples

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

Don't know the UniProt ID? Use [getSequence] and pipe into `affetch`
```bash
getseq human top2a, mouse top2a, rat top2a | affetch -
```
*Pipe input arguments must be indicated with a dash `-`*

## Development TODOs

These are some of the much need improvements that I plan to implement in the next release

* Add unit tests

Annoying bug in `Typer` that breaks path completion with the `-o` option: [Typer Issue 951](https://github.com/fastapi/typer/issues/951)

### Credits

Inspired by [getSequence], created with [The Hatchlor] template.

[getSequence]: https://github.com/alexholehouse/getSequence
[The Hatchlor]: https://github.com/florianwilhelm/the-hatchlor