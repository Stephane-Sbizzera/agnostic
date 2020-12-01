resource "random_uuid" "hdi-deploymentid" { }
  
resource "azurerm_resource_group" "hdirg" {
    name = "${var.prefix}-hdi-rg"
    location = var.location
}

resource "azurerm_template_deployment" "hdi" {
  name                = "${var.prefix}hdideploy-${random_uuid.hdi-deploymentid.result}"
  resource_group_name = azurerm_resource_group.hdirg.name
  parameters = {
      "clusterName" = "${var.prefix}hdi"
      "clusterLoginUserName" = var.hdi_cluster_username
      "clusterLoginPassword" = var.hdi_cluster_password
      "sshUserName" = var.hdi_ssh_username    
      "sshPassword" =  var.hdi_ssh_password
      "existingSQLServerResourceGroup" = "${var.prefix}-rg"
      "existingSQLServerName" = "${var.prefix}sqlsrv"
      "existingSQLServerUsername" = var.sql_username
      "existingSQLServerPassword" = var.sql_password
      "existingAmbariSqlDBName" = "${var.prefix}ambarisqldb"
      "existingVirtualNetworkResourceGroup" = "${var.prefix}-rg"
      "existingAdlsGen2StgAccountResourceGroup" = "${var.prefix}-rg"
      "existingAdlsGen2StgAccountname" = "${var.prefix}stg"
      "newOrExistingAdlsGen2FileSystem" = "${var.prefix}fs"
      "existingHdiUserManagedIdentityResourceGroup" = "${var.prefix}-rg"
      "existingHdiUserManagedIdentityName" = "${var.prefix}hdiumi"
   }
  deployment_mode = "Incremental"
}
