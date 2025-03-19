from decimal import Decimal
import os
import sys

from lxml import etree
from tqdm import tqdm
from logging import Logger

sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from conf import CONFIG


def find_assets_names(xbrl_folder: str, logger: Logger) -> set:
    """
    Parses XBRL files in the specified folder and extracts unique tag values.

    :param xbrl_folder: Path to the folder containing XBRL files.
    :param logger: Logger instance for logging.
    :return: A set of unique tag values.
    """
    logger.info(f'Started parsing folder: {xbrl_folder}')
    unique_assets = set()

    if not os.path.exists(xbrl_folder):
        raise FileNotFoundError(f'Folder {xbrl_folder} does not exist.')

    print('Parsing XBRLs...')
    for file_name in tqdm(os.listdir(xbrl_folder)):
        file_path = os.path.join(xbrl_folder, file_name)

        if file_path.lower().endswith('.xbrl'):
            logger.debug(f'Processing file: {file_path}')
            try:
                tree = etree.parse(file_path)
                root = tree.getroot()

                namespaces = {'jenv-bw2-i': 'http://example.com/jenv-bw2-i'}
                xpath_expr = "//*[contains(name(), ':')][@contextRef and @decimals and @unitRef]"
                elements = root.xpath(xpath_expr, namespaces=namespaces)
                unique_assets.update(element.tag.split('}')[-1]
                                     for element in elements if element.tag)
            except etree.XMLSyntaxError as e:
                logger.error(f"Error parsing file '{file_path}': {str(e)}")

    return unique_assets


def get_asset_group(asset_name: str) -> str:
    """
    Aligns asset to one of the groups defined in config

    :param asset_name: Name of the asset.
    :return: Assigned group (or Others if not found).
    """
    asset_group = 'others'
    for asset in CONFIG['balancesheet_columns'].keys():
        if asset_name in CONFIG['balancesheet_columns'][asset]:
            asset_group = asset
            break
    # if asset_name in CONFIG['balancesheet_columns']['assets']:
    #     asset_group = 'Asset'
    # elif asset_name in CONFIG['balancesheet_columns']['liabilities']:
    #     asset_group = 'Liability'
    # elif asset_name in CONFIG['balancesheet_columns']['equities']:
    #     asset_group = 'Equity'

    return asset_group


def revert_decimal(value: float, decimals: str) -> Decimal:
    """
    Revert shifted decimal to standard position according to the xbrl doc:
    https://www.xbrl.org/WGN/precision-decimals-units/WGN-2017-01-11/precision-decimals-units-WGN-2017-01-11.html#regulator-accuracy

    :param value: Shifted value
    :param decimals: given decimal.
    :return: Unshifted decimal.
    """
    if decimals == "INF":
        return Decimal(value)
    else:
        scale = Decimal("10") ** Decimal(decimals)
        return Decimal(value) / scale
