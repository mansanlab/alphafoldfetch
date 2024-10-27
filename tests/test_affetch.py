import gzip
from pathlib import Path
from unittest.mock import AsyncMock

import aiohttp
import pytest

from affetch.main import (
    alphafold_api,
    alphafold_api_call,
    alphafold_api_coroutine,
    alphafold_api_url,
    alphfold_file_url,
    app,
    chunk_urls,
    validate_fasta,
    validate_uniprot_id,
    write_gz_structure,
    write_structure,
)
