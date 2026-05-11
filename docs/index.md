# AlphaFoldFetch

AlphaFoldFetch is a small command-line tool for downloading AlphaFold structure files from UniProt accessions or UniProt-style FASTA files.

Use it when you want to:

- download one or many AlphaFold structures from the terminal
- save PDB files, CIF files, or both
- gzip outputs for batch jobs
- feed IDs from FASTA files or stdin

## Quick Start

Run it once with `uvx`:

```bash
uvx --from AlphaFoldFetch affetch P11388
```

Or, after installation:

```bash
affetch P11388 Q01320 P41516
```

By default, AlphaFoldFetch downloads gzipped PDB and CIF files for AlphaFold model 6:

```text
AF-P11388-F1-model_v6.pdb.gz
AF-P11388-F1-model_v6.cif.gz
```

## Common Tasks

Download an uncompressed PDB only:

```bash
affetch -f p P11388
```

Download structures listed in a FASTA file:

```bash
affetch UP000005640_9606.fasta
```

Read IDs from stdin:

```bash
printf "P11388\nQ01320\n" | affetch -
```

## Next Steps

- [Install AlphaFoldFetch](installation.md)
- [Learn the CLI options and input rules](usage.md)
- [Set up a development environment](development.md)
