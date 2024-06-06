# Usage
python -m update_csa_details

# Prerequisites:
Update the mapping of uuid to account id of the account updated during credentialing here "./uuid_account_mapping.json"
ex: { "uuid" : "account_id" }

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
