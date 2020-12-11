resource "azurerm_subnet" "subnet" {
  name                      = "akc-${terraform.workspace}-subnet"
  resource_group_name       = "${var.res_group_name}"
  virtual_network_name      = "${var.vnet_name}"
  address_prefix            = "${var.subnet_prefixes[terraform.workspace]}"
}