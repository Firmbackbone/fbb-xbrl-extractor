from logging import Logger
import os
import uuid
import zipfile

from tqdm import tqdm


class ZipXMLExtractor:
    """Utility class to extract .xbrl files from ZIP archives."""

    @staticmethod
    def extract(source_path: str, dest_path: str, logger: Logger) -> None:
        """
        Extracts .xbrl files from ZIP archives in a source directory
        to a destination directory.

        :param source_path: Path to the directory containing ZIP files.
        :param dest_path: Path to the directory for extracted files.
        :param logger: Logger instance for logging.
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
                ZipXMLExtractor._extract_zip(file_path, dest_path, logger)
            else:
                logger.warning(f"Skipping non-ZIP file: {file_name}")

    @staticmethod
    def _extract_zip(file_path: str, dest_path: str, logger: Logger) -> None:
        """Extracts .xbrl files from a single ZIP file."""
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                xbrl_files = [
                    member for member in zip_ref.namelist()
                    if member.endswith('.xbrl') and not member.endswith('/')
                ]

                if not xbrl_files:
                    logger.warning(f"No .xbrl files in ZIP: {os.path.basename(file_path)}")
                    return

                for member in xbrl_files:
                    output_file_path = os.path.join(dest_path, f"{uuid.uuid4().hex}.xbrl")
                    try:
                        with zip_ref.open(member) as source, open(output_file_path, 'wb') as target:
                            target.write(source.read())
                        logger.info(f"Extracted {member} to '{output_file_path}'")
                    except Exception as e:
                        logger.error(f"Error extracting '{member}': {e}")
        except zipfile.BadZipFile as e:
            logger.error(f"Invalid ZIP file '{file_path}': {e}")
