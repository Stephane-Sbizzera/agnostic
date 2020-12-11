resource "azurerm_storage_account" "example" {
  name                     = "st-${terraform.workspace}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_share" "example" {
  name                 = "sts-${terraform.workspace}"
  storage_account_name = azurerm_storage_account.example.name
  quota                = 50

  acl {
    id = "2b2ee77d-8520-4459-a035-26afd4fb051e"

    access_policy {
      permissions = "rwdl"
      start       = "2019-07-02T09:38:21.0000000Z"
      expiry      = "2019-07-02T10:38:21.0000000Z"
    }
  }
}