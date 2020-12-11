
docker pull zenika/terraform-azure-cli:latest
docker container run -it --rm --mount type=bind,source="$(pwd)",target=/workspace zenika/terraform-azure-cli:latest


RESOURCE_GROUP_NAME="Terraform"
STORAGE_ACCOUNT="terraformaccountx"
export ARM_SUBSCRIPTION_ID="6c5c1c25-0d56-4a79-92f5-27fc017d2289"
az login 

az account list --output table

az account set --subscription $ARM_SUBSCRIPTION_ID
az ad sp create-for-rbac --name terraform --scopes="/subscriptions/$ARM_SUBSCRIPTION_ID"
az ad sp create-for-rbac --skip-assignment

az group create --name $RESOURCE_GROUP_NAME --location "eastus"
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT 

ACCOUNT_KEY=$(az storage account keys list -g $RESOURCE_GROUP_NAME -n $STORAGE_ACCOUNT --query '[0].value' -o tsv)

az storage container create -n tfstate --account-name $STORAGE_ACCOUNT --account-key $ACCOUNT_KEY

export ARM_CLIENT_ID=$(az ad sp list --query "[?appDisplayName == 'terraform']|[].appId" --out tsv)
export ARM_TENANT_ID=$(az ad sp list --display-name terraform --query "[].appOwnerTenantId" --out tsv) 
export ARM_CLIENT_NAME_ID=$(az ad sp list --query "[?appDisplayName == 'terraform']|[].appId" --out tsv)
printenv | grep ARM

terraform init -backend-config=backend.tfvars
terraform workspace new dev
terraform apply -auto-approve