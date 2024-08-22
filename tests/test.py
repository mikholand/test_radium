"""Покрытие тестами для тестового задания."""
import hashlib
import os
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from aioresponses import aioresponses

from main import calculate_file_hash, download_file, main

FILE_CONTENT = b'file_content'
URL = os.getenv('URL')


@pytest.mark.asyncio
async def test_download_file(tmp_path: Path):
    """Тест для функции скачивания файла."""
    file_path = tmp_path / 'project-configuration_0.zip'

    with aioresponses() as mock:
        mock.get(URL, body=FILE_CONTENT)

        await download_file(URL, file_path)

    assert file_path.exists()
    assert file_path.read_bytes() == FILE_CONTENT


@pytest.mark.asyncio
async def test_calculate_file_hash(tmp_path: Path):
    """Тест для функции подсчета хеша файла."""
    file_path = tmp_path / 'project-configuration_1.zip'
    file_path.write_bytes(FILE_CONTENT)

    expected_hash = hashlib.sha256(FILE_CONTENT).hexdigest()

    _, calculated_hash = await calculate_file_hash(file_path)
    assert calculated_hash == expected_hash


@pytest.mark.asyncio
async def test_main(mocker):
    """Тест для главной функции."""
    mocker.patch('main.download_file', new_callable=AsyncMock)
    mocker.patch('main.calculate_file_hash', return_value=('file', 'hash'))

    main_results = await main(3)
    assert len(main_results) == 3
    assert all(hash_value == 'hash' for _, hash_value in main_results)
