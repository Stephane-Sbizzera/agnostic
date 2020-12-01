resource "azurerm_user_assigned_identity" "hdi-usermanagedidentity" {
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  name = "${var.prefix}hdiumi"
}

resource "azurerm_storage_account" "stg2" {
  name                     = "${var.prefix}stg2"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = "true"


}

resource "azurerm_role_assignment" "stg_auth_hdiuseridentity" {
  scope                = azurerm_storage_account.stg2.id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = azurerm_user_assigned_identity.hdi-usermanagedidentity.principal_id  
}
