import json

DB_CONFIG = {}

# { "uuid" : "account_id" }
UUID_MAPPING = {"00001": '820842078405',
                "00002": '375971864783'}

TRUSTEE_ACCOUNT_ID = "TRUSTEE_ACCOUNT_ID"


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


def connect_to_db(config):
    # TODO: Create dynamodb client
    conn = "dynamodb_connect"
    return conn


def update_account_data(conn, uuid, trustee_id, role_name, external_id):
    # TODO: Implement dynamodb update operation for columns trustee_id, role_name, external_id
    print(f"{uuid}: {trustee_id}, {role_name}, {external_id}")


def main():
    # Read data from JSON file
    csa_cldy_customer_data = _read_json_file('./csa-and-cldy-customers-data.json')
    csa_customer_data = _read_json_file('./csa-only-customers-data.json')
    all_customer_data = csa_cldy_customer_data + csa_customer_data

    # Process Data for parent account details and linked account details
    accounts_data = extract_account_data(all_customer_data)

    # Connect to the database
    conn = connect_to_db(DB_CONFIG)

    # Insert data into the dynamodb for the given uuid of the record
    for uuid, account_id in UUID_MAPPING.items():
        trustee_id, role_name, external_id = (accounts_data.get(account_id))
        try:
            update_account_data(conn, uuid, trustee_id, role_name, external_id)
        finally:
            pass
            # conn.close()


if __name__ == "__main__":
    main()
