
# Requirements
- Docker
- Kubectl

# Install Docker and run
- docker pull zenika/terraform-azure-cli:latest
- docker container run -it --rm --mount type=bind,source="$(pwd)",target=/workspace zenika/terraform-azure-cli:latest

# Execute the commands below
RESOURCE_GROUP_NAME="Terraform"  
STORAGE_ACCOUNT="terraformaccountx"  
export ARM_SUBSCRIPTION_ID="6c5c1c25-0d56-4a79-92f5-27fc017d2289"  
az login   
az account list --output table  
az account set --subscription $ARM_SUBSCRIPTION_ID  

az group create --name $RESOURCE_GROUP_NAME --location "eastus"  
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT   

ACCOUNT_KEY=$(az storage account keys list -g $RESOURCE_GROUP_NAME -n $STORAGE_ACCOUNT --query '[0].value' -o tsv)  
az storage container create -n tfstate --account-name $STORAGE_ACCOUNT --account-key $ACCOUNT_KEY  

# Setup

This repo is a companion repo to the [Provision an AKS Cluster learn guide](https://learn.hashicorp.com/terraform/kubernetes/provision-aks-cluster), containing
Terraform configuration files to provision an AKS cluster on
Azure.

After installing the Azure CLI and logging in. Create an Active Directory service
principal account.

```shell
$ az ad sp create-for-rbac --name terraform --scopes="/subscriptions/$ARM_SUBSCRIPTION_ID"
{
  "appId": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "displayName": "azure-cli-2019-04-11-00-46-05",
  "name": "http://azure-cli-2019-04-11-00-46-05",
  "password": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "tenant": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
}
```

export ARM_CLIENT_ID=$(az ad sp list --query "[?appDisplayName == 'terraform']|[].appId" --out tsv)  
export ARM_TENANT_ID=$(az ad sp list --display-name terraform --query "[].appOwnerTenantId" --out tsv)   
export ARM_CLIENT_NAME_ID=$(az ad sp list --query "[?appDisplayName == 'terraform']|[].appId" --out tsv)  
printenv | grep ARM  

Then, replace `terraform.tfvars` values with your `client_id`,`tenant_id`, `client_secret` and `client_secret`. 
Terraform will use these values to provision resources on Azure.

After you've done this, initalize your Terraform workspace, which will download 
the provider and initialize it with the values provided in the `terraform.tfvars` file.

```shell
$ terraform init -backend-config=backend.tfvars
$ terraform workspace new dev

Initializing provider plugins...
- Checking for available provider plugins on https://releases.hashicorp.com...
- Downloading plugin for provider "azurerm" (1.27.0)...

Terraform has been successfully initialized!
```

Then, provision your AKS cluster by running `terraform apply -auto-approve`. This will 
take approximately 10 minutes.

```shell
$ terraform apply -auto-approve

# Output truncated...

Plan: 3 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

# Output truncated...

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

Outputs:

kubernetes_cluster_name = xxx
resource_group_name = xxx
```

## Configure kubectl

To configure kubetcl run the following command:

```shell
$ az aks get-credentials --resource-group aks-dev --name k8s-dev;
```

The
[resource group name](https://github.com/hashicorp/learn-terraform-provision-aks-cluster/blob/master/aks-cluster.tf#L16)
and [AKS name](https://github.com/hashicorp/learn-terraform-provision-aks-cluster/blob/master/aks-cluster.tf#L25)
 correspond to the output variables showed after the successful Terraform run.

You can view these outputs again by running:

```shell
$ terraform output
```

## Configure Kubernetes Dashboard

To use the Kubernetes dashboard, we need to create a `ClusterRoleBinding`. This
gives the `cluster-admin` permission to access the `kubernetes-dashboard`.

```shell
$ kubectl create clusterrolebinding kubernetes-dashboard --clusterrole=cluster-admin --serviceaccount=kube-system:kubernetes-dashboard  --user=clusterUser

```

Finally, to access the Kubernetes dashboard, run the following command:

```shell
$ az aks browse --resource-group aks-dev --name k8s-dev
Proxy running on http://127.0.0.1:8001/
Press CTRL+C to close the tunnel...
```

# Login
Run `kubectl config view` to get the token and access the dashboard

 You should be able to access the Kubernetes dashboard at [http://127.0.0.1:8001/](http://127.0.0.1:8001/).
