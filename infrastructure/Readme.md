Sample scripts to create and HDInsight environment as shown in the following architecture diagram.


**Environment Creation**
1. Download Terraform - https://www.terraform.io/
2. Download the folder/repo to local machine
3. Download Azure CLI - https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
4. Go over the *variable.tf* file and update the values as per your environment, the file itself has instructions in the comments
5. On a Terminal go to the *hdinsight* folder 
6. Run the command *az login*
7. Run the command *az account set -s <subscriptionid or name>* (Optional - only if you have multiple subscriptions and you want to use non-default Azure Subscription)
7. Run the command *terraform init*
8. Run the command *terraform apply* to create the environment

Following resources are created as part of these scripts
- Azure VNET with Subnets and NSGs
- Azure Virtual Machine with Network Interface Card
- Azure Bastion with Public IP
- Azure HDInsight Cluster with Load Balancers, Public IP, Network Interface Cards, etc.
- Azure SQL Database with logical server
- Azure Data Lake Gen2 (storage account)
- User Managed Identity for Azure HDInsight
