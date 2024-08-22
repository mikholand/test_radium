"""Тестовое задание для скачивания из репозитория и подсчета хеш-функции."""
import asyncio
import hashlib
import logging
import os
from pathlib import Path

import aiohttp
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

FOLDER_NAME = os.getenv('FOLDER_NAME')
URL = os.getenv('URL')

# Настройка логирования для отслеживания событий и ошибок.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def download_file(url: str, file_path: Path, retries: int = 3) -> None:
    """
    Скачивает содержимое с указанного URL и сохраняет его в файл.

    Args:
        url (str): URL для скачивания.
        file_path (Path): Путь для сохранения файла.
        retries (int): Количество попыток при неудаче. По умолчанию 3.

    Raises:
        aiohttp.ClientError: В случае проблем с сетью или сервером.
    """
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    file_content = await response.read()
                    file_path.write_bytes(file_content)
                    logger.info('Скачан файл: {0}'.format(file_path))
                    return
        except aiohttp.ClientError as client_error:
            logger.error(
                'Ошибка при скачивании файла {0}: {1}'.format(
                    file_path, client_error,
                ),
            )
            if attempt < retries - 1:
                logger.info('Повторная попытка {0}...'.format(attempt + 1))
                await asyncio.sleep(1)
            else:
                raise


async def calculate_file_hash(file_path: Path) -> tuple[str, str]:
    """
    Считает sha256 хеш для указанного файла.

    Args:
        file_path (Path): Путь к файлу.

    Returns:
        tuple: Путь к файлу и его хеш.
    """
    file_content = file_path.read_bytes()
    hash_sum = hashlib.sha256(file_content).hexdigest()
    logger.info('Подсчитан хеш для файла {0}'.format(file_path))
    return str(file_path), hash_sum


async def prepare_files(num_files: int) -> list[Path]:
    """
    Создает временную папку и формирует список файлов.

    Args:
        num_files (int): Количество файлов для подготовки.

    Returns:
        list[Path]: Список путей к файлам.
    """
    folder_path = Path(FOLDER_NAME)
    folder_path.mkdir(parents=True, exist_ok=True)

    files = [
        folder_path / 'project-configuration_{0}.zip'.format(file_index)
        for file_index in range(num_files)
    ]
    logger.info(
        'Подготовлено {0} файлов в папке {1}'.format(num_files, folder_path),
    )

    return files


async def main(num_tasks: int) -> list[tuple[str, str]]:
    """
    Главная функция для скачивания файлов и подсчета их хеш-функций.

    Args:
        num_tasks (int): Количество задач для выполнения.

    Returns:
        list[tuple[str, str]]: Список пар (путь к файлу, его хеш).
    """
    file_paths = await prepare_files(num_tasks)

    download_tasks = [
        asyncio.create_task(download_file(URL, file_path))
        for file_path in file_paths
    ]
    await asyncio.gather(*download_tasks)

    hash_tasks = [
        asyncio.create_task(calculate_file_hash(file_path))
        for file_path in file_paths
    ]

    return await asyncio.gather(*hash_tasks)


if __name__ == '__main__':
    hash_results = asyncio.run(main(3))
    for file_path, file_hash in hash_results:
        logger.info('Файл: {0}, SHA256: {1}'.format(file_path, file_hash))
