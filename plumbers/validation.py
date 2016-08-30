from datapackage import DataPackage
from datapackage.exceptions import ValidationError
from goodtables.pipeline import Pipeline
from pandas.core import index
from tellme import Report
from cchardet import detect
from logging import debug
from odo import odo, resource
from pandas import read_excel, Index

from jsontableschema.exceptions import (InvalidSchemaError,
                                        SchemaValidationError)


SOURCE_SCHEMA = '/home/loic/repos/eu-structural-funds/' \
                 'data/be/BE1.bruxelles/source.schema.json'
SOURCE_DATA = '/home/loic/repos/eu-structural-funds/' \
              'data/be/BE1.bruxelles/Liste des bénéficiaires.xls'

EXTRACT_FILE = '/home/loic/repos/eu-structural-funds/' \
              'data/be/BE1.bruxelles/extract.data.csv'
SOURCE_REPORT = '/home/loic/repos/eu-structural-funds/' \
              'data/be/BE1.bruxelles/extract.report.json'

COMMENT_LINES = [0, 1, 2, 3, 6, 15, 16, 22, 23, 29]


def detect_encoding(filepath):
    with open(filepath, 'rb') as file:
        bytes_ = file.read()
    detected_encoding = detect(bytes_)['encoding']
    debug(detected_encoding)
    return detected_encoding


def validate_data(data, schema):
    report_stream = open(SOURCE_REPORT, 'w+')
    pipeline = Pipeline(data, report_stream=report_stream)
    pipeline.register_processor('schema', options={'schema': schema})
    valid, report = pipeline.run()
    return valid, report


def validate_schema(package):
    try:
        package.validate()
        return []
    except (ValidationError, InvalidSchemaError, SchemaValidationError):
        for error in package.iter_errors():
            yield error.message


if __name__ == '__main__':
    package_ = DataPackage(SOURCE_SCHEMA)
    encoding_ = detect_encoding(SOURCE_DATA)
    errors_ = list(validate_schema(package_))

    source_df = read_excel(SOURCE_DATA, header=4, skiprows=range(0, 3))
    comment_lines = source_df.index[COMMENT_LINES]
    for i in COMMENT_LINES:
        print(list(source_df.iloc[i]))
    source_df = source_df.drop(comment_lines)
    source_csv = SOURCE_DATA.replace('xls', 'csv')
    source_df.to_csv(source_csv)

    odo(source_df, source_csv)

    if errors_:
        for message in errors_:
            print('Schema error:', message)
    else:
        print('Valid schema:', SOURCE_SCHEMA)

    for resource in package_.descriptor['resources']:
        with open(source_csv, encoding=encoding_) as source_stream:
            valid_, report_ = validate_data(SOURCE_DATA, resource['schema'])
            print(valid_)
