from datetime import datetime
import logging

from conf import CONFIG
from src.extractors import ZipXMLExtractor
from src.parsers import XBRLParser


def main():
    handler = logging.FileHandler(f"logs/run_{datetime.now().strftime('%d%m%YT%H%M%S')}.log")
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger('XBRLLogger')
    logger.setLevel(CONFIG['logger']['level'])
    logger.addHandler(handler)

    zip_dir = CONFIG['data']['zip_path']
    extract_dir = CONFIG['data']['dest_path']

    ZipXMLExtractor.extract(zip_dir, extract_dir, logger)
    XBRLParser.parse_xbrl(extract_dir, logger)


if __name__ == '__main__':
    main()
