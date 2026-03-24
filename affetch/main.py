import asyncio
import concurrent
import functools
import gzip
import http
import itertools
import re
import sys
from collections.abc import Callable, Generator, Iterable
from pathlib import Path
from typing import Final

import aiohttp
import typer

from affetch import __version__

CLI_NAME: Final[str] = f"AlphaFoldFetch {__version__}"
UniProtId = str
AlphaFoldUrl = str
SUPPORTED_MODELS: Final[tuple[int, ...]] = (1, 2, 3, 4, 5, 6)
SUPPORTED_MODEL_TEXT: Final[str] = ", ".join(str(model) for model in SUPPORTED_MODELS)
ResultMap = dict[AlphaFoldUrl, str]
StructureWriter = Callable[[Path, str], None]

app = typer.Typer(
    name=CLI_NAME,
    help="A tool for downloading AlphaFold structures using UniProt IDs or FASTA files",
)

# Base URL for the AlphaFold API - holding on for later use
ALPHAFOLD_API_URL: Final[str] = "https://alphafold.ebi.ac.uk/api/prediction/"

# Public AlphaFold API key - holding on for later use
API_KEY: Final[str] = "AIzaSyCeurAJz7ZGjPQUtEaerUkBZ3TaBkXrY94"

# Base URL for the AlphaFold file server
ALPHAFOLD_FILE_URL: Final[str] = "https://alphafold.ebi.ac.uk/files/"

# Validation regex for UniProt IDs
UNIPROT_RE_STR: Final[str] = r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"
UNIPROT_RE: Final[re.Pattern[str]] = re.compile(UNIPROT_RE_STR)

# Validation suffixes for FASTA Files
FASTA_SUFFIX: Final[tuple[str, ...]] = (".fasta", ".fas", ".fa", ".faa")


def chunk_urls(urls: list[AlphaFoldUrl], n: int) -> Generator[list[AlphaFoldUrl], None, None]:
    """ Split a list of urls into chunks of size N """
    for i in range(0, len(urls), n):
        yield urls[i : i + n]


def alphafold_api_url(uniprot: UniProtId) -> AlphaFoldUrl:
    """ Create AlphaFold API URLs """
    return f"{ALPHAFOLD_API_URL}{uniprot}?key={API_KEY}"


def alphafold_file_url(uniprot: UniProtId, model: int, file: str) -> AlphaFoldUrl:
    """ Create AlphaFold structure file URLs """
    return f"{ALPHAFOLD_FILE_URL}AF-{uniprot}-F1-model_v{model}.{file}"


def alphfold_file_url(uniprot: UniProtId, model: int, file: str) -> AlphaFoldUrl:
    """Backward-compatible alias for the historical misspelling."""
    return alphafold_file_url(uniprot, model, file)


def parse_uniprot(uniprot: str) -> UniProtId:
    """ Parse UniProt IDs with regular expressions """
    uniprot_match = re.search(UNIPROT_RE, uniprot)
    if uniprot_match:
        return uniprot_match.group()
    return ""


def validate_uniprot_id(uniprot: str) -> bool:
    """ Validate UniProt IDs with regular expressions """
    return re.fullmatch(UNIPROT_RE, uniprot) is not None


def validate_fasta(fasta: str) -> list[UniProtId]:
    """ Read a FASTA file and return only valid UniProt IDs """
    uniprot_ids = []
    with open(Path(fasta), encoding="utf-8") as open_fasta:
        for line in open_fasta:
            if line.startswith(">"):
                uniprot_id = parse_uniprot(line)
                if validate_uniprot_id(uniprot_id):
                    uniprot_ids.append(uniprot_id)

    return uniprot_ids


def write_structure(file_path: Path, structure: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(structure)


def write_gz_structure(file_path: Path, structure: str) -> None:
    file_path = Path(f"{file_path}.gz")
    with gzip.open(file_path, "wb") as f:
        f.write(structure.encode("utf-8"))


async def alphafold_api_coroutine(
        session: aiohttp.ClientSession,
        sem: asyncio.Semaphore,
        url: str,
        results: ResultMap
) -> None:
    async with sem, session.get(url) as response:
        if response.status == http.HTTPStatus.OK:
            results[url] = await response.text()


async def alphafold_api_call(
        sem: asyncio.Semaphore,
        urls: list[str],
        results: ResultMap
) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = [alphafold_api_coroutine(session, sem, url, results) for url in urls]
        await asyncio.gather(*tasks)


async def alphafold_api(
        urls: list[str],
        n_sync: int
) -> dict[str, str]:
    sem = asyncio.Semaphore(n_sync)
    results: ResultMap = {}
    await alphafold_api_call(sem, urls, results)
    return results


Uniprot: Final = typer.Argument(..., help="UniProt ID(s) or FASTA file(s)", allow_dash=True)
Output: Final = typer.Option(Path("."), "--output", "-o", help="Output directory", dir_okay=True, exists=True)
FileType: Final = typer.Option("pcz", "--file-type", "-f", help="File type(s), `p` = .pdb, `c` = .cif, `z` = *.gz")
Model: Final = typer.Option(6, "--model", "-m", help=f"AlphaFold model version, ({SUPPORTED_MODEL_TEXT})")
NSync: Final = typer.Option(50, help="Syncronized number of downloads, lower value = slower download speed")
NSave: Final = typer.Option(500, help="Concurrent number of file writes, lower value = slower write speed")


@app.command()
def affetch(
    uniprot: list[str] = Uniprot,
    *,
    output: Path = Output,
    file_type: str = FileType,
    model: int = Model,
    n_sync: int = NSync,
    n_save: int = NSave,
):

    if not any(True for s in "pc" if s in file_type):
        typer.echo("No valid tile type options entered: --file-type must contain `p` and/or `c`", err=True)
        sys.exit(1)

    if model not in SUPPORTED_MODELS:
        typer.echo(f"No valid model options entered: --model must be one of {SUPPORTED_MODEL_TEXT}", err=True)
        sys.exit(1)

    if not output.exists():
        typer.echo(f"No directory named `{output.resolve()}` found", err=True)
        sys.exit(1)

    uniprot_ids: list[str] = []
    if uniprot == ["-"]:
        uniprot = [u.strip() for u in sys.stdin.read().split()]

    for u in uniprot:
        if any(u.endswith(s) for s in FASTA_SUFFIX):
            # If the input is a file, parse it, validate it, and save it
            uniprot_ids += validate_fasta(u)
            continue

        _u = u.upper()
        if validate_uniprot_id(_u):
            # If the input is a string, validate it, and save it
            uniprot_ids.append(_u)
        else:
            # Otherwise, parse it, then validate and save it
            _u = parse_uniprot(_u)
            if validate_uniprot_id(_u):
                uniprot_ids.append(_u)

    if not len(uniprot_ids):
        typer.echo("No valid UniProt IDs entered", err=True)
        sys.exit(1)

    uniprot_urls: Iterable[str] = ()
    if "p" in file_type:
        pdb_url_func = functools.partial(alphafold_file_url, model=model, file="pdb")
        pdb_urls = map(pdb_url_func, uniprot_ids)
        uniprot_urls = itertools.chain(uniprot_urls, pdb_urls)

    if "c" in file_type:
        cif_url_func = functools.partial(alphafold_file_url, model=model, file="cif")
        cif_urls = map(cif_url_func, uniprot_ids)
        uniprot_urls = itertools.chain(uniprot_urls, cif_urls)

    write_func: StructureWriter = write_structure
    if "z" in file_type:
        write_func = write_gz_structure

    for urls in chunk_urls(list(uniprot_urls), n_save):
        structures = asyncio.run(alphafold_api(urls, n_sync))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for url, structure in structures.items():
                file_name = Path(url).name
                file_path = output.joinpath(file_name)
                executor.submit(write_func, file_path, structure)
