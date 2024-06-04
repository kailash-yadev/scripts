# Usage

Prerequisites:
Update the mapping of uuid to account id of the account updated during credentialing here "./uuid_account_mapping.json"
ex: { "uuid" : "account_id" }

# Note: Update the Constants with your specs
ENDPOINT_URL = "http://localhost:8000"
TABLE_NAME = "Accounts"
PARTITION_KEY = "UUID"
PARTITION_KEY_TYPE = "S"
ROLE_NAME_ATTRIBUTE = "RoleName"
EXTERNAL_ID_ATTRIBUTE = "ExternalID"
TRUSTEE_ID_ATTRIBUTE = "TrusteeID"


Sample table Items after update"
{'TrusteeID': {'S': '282711413064'}, 'RoleName': {'S': 'all-lsc-host-cloudability-csa-role-1'}, 'UUID': {'S': '00001'}, 'ExternalID': {'S': 'ext-e7rss8g685'}}
{'TrusteeID': {'S': '282711413064'}, 'RoleName': {'S': 'Share-Cloudwiry-Read-Role'}, 'UUID': {'S': '00002'}, 'ExternalID': {'S': 'CW_AiuYTgyI'}}
