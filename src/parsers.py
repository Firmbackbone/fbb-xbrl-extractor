from copy import copy
from datetime import datetime
from logging import Logger
import os
import re
import sys

from lxml import etree
import pandas as pd

from tqdm import tqdm

sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from conf import CONFIG
from src.utils import get_asset_group, revert_decimal


class XBRLParser:
    """Parser for extracting and processing data from XBRL files."""

    @staticmethod
    def parse_xbrl(xbrl_folder: str, logger: Logger) -> None:
        """
        Parses XBRL files in the specified folder and saves data to a CSV file.

        :param xbrl_folder: Path to the folder containing XBRL files.
        :param logger: Logger instance for logging.
        """
        logger.info(f'Started parsing folder: {xbrl_folder}')
        result_list = []

        if not os.path.exists(xbrl_folder):
            raise FileNotFoundError(f'Folder {xbrl_folder} does not exist.')

        print('Parsing XBRLs...')
        for file_name in tqdm(os.listdir(xbrl_folder)):
            file_path = os.path.join(xbrl_folder, file_name)

            if file_path.lower().endswith('.xbrl'):
                logger.debug(f'Processing file: {file_path}')
                try:
                    XBRLParser._parse_file(file_path, result_list, logger)
                except etree.XMLSyntaxError as e:
                    logger.error(f"Error parsing file '{file_path}': {str(e)}")

        XBRLParser._save_to_csv(result_list, logger)

    @staticmethod
    def _parse_file(file_path: str, result_list: list, logger: Logger) -> None:
        """Parses a single XBRL file and extracts relevant data."""
        tree = etree.parse(file_path)
        root = tree.getroot()

        entity_data = {}
        entity_data['Filename'] = re.search(r'[a-f0-9]{32}', file_path).group()
        for xbrl_name, csv_name in CONFIG['base_columns'].items():
            value = ''
            for element in root.xpath(f".//*[local-name()='{xbrl_name}']"):
                if element.text:
                    value = element.text.strip()
                    if value:
                        break

            csv_name = xbrl_name if not csv_name else csv_name
            if not value:
                logger.warning(f'{xbrl_name} not found in {file_path}.')
            entity_data[csv_name] = value

        assets_namespaces = {'jenv-bw2-i': 'http://example.com/jenv-bw2-i'}
        assets_expr = "//*[contains(name(), ':')][@contextRef and @decimals and @unitRef]"
        for element in root.xpath(assets_expr, namespaces=assets_namespaces):
            asset_name = element.tag.split('}')[-1]
            asset_raw_value = element.text.strip() if element.text else None
            asset_context = element.get("contextRef")
            asset_currency_context = element.get("unitRef")
            asset_decimals = element.get('decimals')

            context_element = root.xpath(f".//*[@id='{asset_context}']")
            asset_start_date = None
            asset_end_date = None
            for element in context_element:
                instant_date_element = element.xpath(".//*[local-name()='instant']")
                start_date_element = element.xpath(".//*[local-name()='startDate']")
                end_date_element = element.xpath(".//*[local-name()='endDate']")

                if instant_date_element:
                    asset_end_date = instant_date_element[0].text.strip()
                if start_date_element:
                    asset_start_date = start_date_element[0].text.strip()
                if end_date_element:
                    end_date_element = end_date_element[0].text.strip()

            currency_context_element = root.xpath(f".//*[@id='{asset_currency_context}']")
            asset_currency = asset_currency_context
            for element in currency_context_element:
                currency_element = element.xpath(".//*[local-name()='measure']")
                if currency_element:
                    asset_currency = currency_element[0].text.split(':')[-1]
                break

            if asset_currency != 'pure':
                asset_value = revert_decimal(asset_raw_value, asset_decimals)
                asset_group = get_asset_group(asset_name)

                asset_data = copy(entity_data)
                asset_data.update({
                    'AssetGroup': asset_group,
                    'AssetType': asset_name,
                    'AssetValue': asset_value,
                    'AssetCurrency': asset_currency,
                    'AssetStartDate': asset_start_date,
                    'AssetEndDate': asset_end_date,
                })
                result_list.append(asset_data)

                logger.debug(f"Found asset data: {asset_name} in {file_path}")

    @staticmethod
    def _save_to_csv(result_list: list, logger: Logger) -> None:
        """Saves parsed data to a CSV file."""
        if result_list:
            df = pd.DataFrame(result_list)
            csv_file_path = f"outputs/output_{datetime.now().strftime('%d%m%YT%H%M%S')}.csv"
            df.to_csv(csv_file_path, index=False, encoding="utf-8", header=True)
            logger.info(f'Data saved to CSV file: {csv_file_path}')
        else:
            logger.warning('No data found to save.')
