from logging import Logger
import os
import uuid
import zipfile
from io import BytesIO

from tqdm import tqdm


class ZipXMLExtractor:
    """Utility class to extract .xbrl files from ZIP archives, including nested ZIPs."""

    @staticmethod
    def extract(source_path: str, dest_path: str, logger: Logger) -> None:
        """
        Extracts .xbrl files from ZIP archives (including nested ZIPs) in a source directory
        to a destination directory.
        """
        os.makedirs(dest_path, exist_ok=True)
        logger.debug(f"Destination directory '{dest_path}' created.")

        if not os.path.exists(source_path):
            logger.error(f"Source folder '{source_path}' does not exist.")
            raise FileNotFoundError(f"Source folder '{source_path}' does not exist.")

        logger.info(f"Starting extraction from '{source_path}'.")

        print('Extracting ZIPs...')
        for file_name in tqdm(os.listdir(source_path)):
            file_path = os.path.join(source_path, file_name)

            if not os.path.isfile(file_path):
                logger.warning(f"Skipping non-file entry: {file_name}")
                continue

            if zipfile.is_zipfile(file_path):
                logger.debug(f"Processing ZIP file: {file_name}")
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        ZipXMLExtractor._extract_zip_archive(zip_ref, dest_path, logger)
                except zipfile.BadZipFile as e:
                    logger.error(f"Invalid ZIP file '{file_name}': {e}")
            else:
                logger.warning(f"Skipping non-ZIP file: {file_name}")

    @staticmethod
    def _extract_zip_archive(zip_ref: zipfile.ZipFile, dest_path: str, logger: Logger) -> None:
        """
        Extracts .xbrl files from a zipfile.ZipFile object. If a nested ZIP file is found,
        it is processed recursively.
        """
        for member in zip_ref.namelist():
            # Skip directory entries
            if member.endswith('/'):
                continue

            # Process nested ZIP file
            if member.lower().endswith('.zip'):
                logger.debug(f"Found nested ZIP: {member}")
                try:
                    # Read the nested zip file into memory
                    nested_zip_data = zip_ref.read(member)
                    with BytesIO(nested_zip_data) as nested_file:
                        with zipfile.ZipFile(nested_file, 'r') as nested_zip:
                            ZipXMLExtractor._extract_zip_archive(nested_zip, dest_path, logger)
                except Exception as e:
                    logger.error(f"Error processing nested ZIP '{member}': {e}")
                continue

            # Extract .xbrl files
            if member.lower().endswith('.xbrl'):
                output_file_path = os.path.join(dest_path, f"{uuid.uuid4().hex}.xbrl")
                try:
                    with zip_ref.open(member) as source, open(output_file_path, 'wb') as target:
                        target.write(source.read())
                    logger.info(f"Extracted {member} to '{output_file_path}'")
                except Exception as e:
                    logger.error(f"Error extracting '{member}': {e}")
            else:
                logger.debug(f"Skipping non-.xbrl and non-ZIP member: {member}")
