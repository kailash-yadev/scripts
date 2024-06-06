import json
import boto3

# CONSTANTS
# Note: Update the Constants with your specs
# Dynamodb endpoint url
ENDPOINT_URL = "http://localhost:8000"

# Table Name in db
TABLE_NAME = "Accounts"

# Partition key or uuid of the account record
PARTITION_KEY = "UUID"
PARTITION_KEY_TYPE = "S"

# Attribute names for rolename, external_id, trustee_id
ROLE_NAME_ATTRIBUTE = "RoleName"
EXTERNAL_ID_ATTRIBUTE = "ExternalID"
TRUSTEE_ID_ATTRIBUTE = "TrusteeID"


# Trustee ID is the same constant for all the customers
TRUSTEE_ACCOUNT_ID = "282711413064"

# TODO: Need to update the mapping of uuid to account id of the account updated during credentialing
# { "uuid" : "account_id" }
# /uuid_account_mapping.json


def _read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data


def _get_account_details(account):
    account_id = account.get('account_id')
    role_arn = account.get('role_arn')
    external_id = account.get('external_id')
    role_name = role_arn.split('role/')[-1]
    return account_id, role_name, external_id


def extract_account_data(customer_data):
    accounts_data = {}
    for org in customer_data:
        for account in org.get('data'):
            parent_account = account.get('parent')
            # parent account details
            if parent_account is not None:
                account_id, csa_role_name, csa_external_id = _get_account_details(parent_account)
                accounts_data[account_id] = [TRUSTEE_ACCOUNT_ID, csa_role_name, csa_external_id]

            for children_account in account.get('children'):
                if children_account is not None:
                    account_id, csa_role_name, csa_external_id = _get_account_details(children_account)
                    accounts_data[account_id] = [TRUSTEE_ACCOUNT_ID, csa_role_name, csa_external_id]
    return accounts_data


def connect_to_db():
    conn = boto3.client('dynamodb', endpoint_url=ENDPOINT_URL)
    return conn


def update_account_data(conn, uuid, trustee_id, role_name, external_id):
    update_expression = "SET #attr1 = :val1, #attr2 = :val2, #attr3 =:val3"
    expression_attribute_names = {"#attr1": ROLE_NAME_ATTRIBUTE, "#attr2": EXTERNAL_ID_ATTRIBUTE, "#attr3": TRUSTEE_ID_ATTRIBUTE}
    expression_attribute_values = {":val1": {"S": role_name}, ":val2": {"S": external_id}, ":val3": {"S": trustee_id}}
    key = {PARTITION_KEY: {PARTITION_KEY_TYPE: uuid}}
    conn.update_item(
        TableName=TABLE_NAME,
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )


def get_updated_record(conn, uuid):
    key = {PARTITION_KEY: {PARTITION_KEY_TYPE: uuid}}
    response = conn.get_item(
        TableName=TABLE_NAME,
        Key=key
    )
    return response.get("Item")


def main():
    # Read data from JSON file
    csa_customer_data = _read_json_file('./csa-and-cldy-customers-data.json')

    # Process Data for parent account details and linked account details
    accounts_data = extract_account_data(csa_customer_data)

    # Connect to the database
    conn = connect_to_db()

    # Read UUID AccountID Mapping
    uuid_mapping = _read_json_file('./uuid_account_mapping.json')
    # Insert data into the dynamodb for the given uuid of the record
    try:
        for uuid, account_id in uuid_mapping.items():
            trustee_id, role_name, external_id = (accounts_data.get(account_id))
            update_account_data(conn, uuid, trustee_id, role_name, external_id)
            print(get_updated_record(conn, uuid))
    finally:
        del conn


if __name__ == "__main__":
    main()
