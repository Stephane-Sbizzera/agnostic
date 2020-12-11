resource "azurerm_postgresql_server" "az_psql" {
  name                = "az-${terraform.workspace}-psql"
  location            = "${var.location}"
  resource_group_name = "${var.res_group_name}"
  sku_name = "B_Gen5_2"

  storage_profile {
    storage_mb            = "${var.pgsql_storage[terraform.workspace]}"
    backup_retention_days = "${var.pgsql_backup[terraform.workspace]}"
    geo_redundant_backup  = "${var.pgsql_redundant_backup[terraform.workspace]}"
  }

  administrator_login          = "psqladmin"
  administrator_login_password = "${var.pgsql_password}"
  version                      = "9.6"
  ssl_enforcement              = "Enabled"

  tags = {
    Environment = "${terraform.workspace}"
  }
}