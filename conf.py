CONFIG = {
    'version': 1,
    'logger': {
        # Logger level: DEBUG=10, INFO=20, WARN=30, ERROR=40
        'level': 10,
    },
    'data': {
        'zip_path': 'data/XBRL Sample',
        'dest_path': 'data/extracted_xbrl',
    },
    'base_columns': {
        # Source from XBRL : Name in output CSV (same if empty)
        'LegalEntityName': '',
        'LegalEntityLegalForm': '',
        'LegalEntityRegisteredOffice': '',
        'ChamberOfCommerceRegistrationNumber': '',
        'LegalSizeCriteriaClassificationSmall': 'LegalEntitySize',
        'StreetNameNL': '',
        'HouseNumberNL': '',
        'PostalCodeNL': '',
        'PlaceOfResidenceNL': '',
        'CountryName': '',
        'BusinessNames': '',
    },
}
