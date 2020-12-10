export AZ_SUBSCRIPTION_ID=$(az account show --query id --out tsv)
RESOURCE_GROUP_NAME="Terraform"
STORAGE_ACCOUNT="terraformaccountx"
az ad sp create-for-rbac --name terraform --role="Contributor" --scopes="/subscriptions/$AZ_SUBSCRIPTION_ID"

az group create --name Terraform --location "Southeast Asia"

az storage account create -n terraformaccountx -g Terraform -l southeastasia --sku Standard_LRS

ACCOUNT_KEY="$(az storage account keys list -g Terraform -n terraformaccountx --query [0].value -o tsv)"

<!-- ACCOUNT_KEY="Qk/Da9Yr0dwMQkZrZHsSrE1jL98Iqus2xMaXhkcrJNKDfPAbFWSU4lU0nRP7Vzn0QGg82xsZoZdrAre3UEKFGg==" -->
az storage container create -n tfstate --account-name terraformaccountx --account-key $ACCOUNT_KEY

export AZ_CLIENT_ID=$(az ad sp list --query "[?appDisplayName == 'terraform']|[].appId" --out tsv)
export AZ_TENANT_ID=$(az ad sp list --display-name terraform --query "[].appOwnerTenantId" --out tsv) 
export AZ_CLIENT_NAME_ID=$(az ad sp list --query "[?appDisplayName == 'terraform']|[].appId" --out tsv)
export AZ_CLIENT_SECRET="45wUKvTLxBW5Zz3.EI9M6nt2hSRM-FI_Eq"


terraform init -backend-config=backend.tfvars

https://github.com/mudrii/akc_sql_terraform