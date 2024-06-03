import json

db_config = {

}

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

def _get_account_details(account):
    account_id = account.get('account_id')
    role_arn = account.get('role_arn')
    external_id = account.get('external_id')
    return account_id, role_arn, external_id

def extract_data(json_data):
    extracted_data = []
    for org in json_data:
        org_id = org.get('org_id')
        for account in org.get('data'):
            parent_account = account.get('parent_account')
            # parent account details
            if parent_account is not None:
                account_id, role_arn, external_id = _get_account_details(parent_account)
                is_parent_account = True
                extracted_data.append((org_id, account_id, role_arn, external_id, is_parent_account))

            for children_account in account.get('children'):
                if children_account is not None:
                    account_id, role_arn, external_id = _get_account_details(children_account)
                    is_parent_account = False
                    extracted_data.append((org_id, account_id, role_arn, external_id, is_parent_account))
    return extracted_data

def connect_to_db(config):
    conn = None
    return conn

def insert_data_to_db(data, conn):
    sql_cmd = "INSERT INTO Accounts(org_id, account_id, role_id, external_id, is_parent) VALUES (%s, %s, %s, %s)"
    # with conn.cusrsor() as cur:
    #     cur.execute(sql_cmd, data)
    #     conn.commit()
    for item in data:
        print(item)

def main():
    # Read data from JSON file
    json_data = read_json_file('/Users/kaiyad/Downloads/csa-and-cldy-customers-data.json')

    # Process Data by column names
    data = extract_data(json_data=json_data)

    # Connect to the database
    conn = connect_to_db(db_config)

    # Insert data into the database
    try:
        insert_data_to_db(data, conn)
    finally:
        pass
        # conn.close()

if __name__ == "__main__":
    main()
