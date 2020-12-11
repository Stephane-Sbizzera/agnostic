resource "azurerm_kubernetes_cluster" "k8s" {
  name                = "k8s-${terraform.workspace}"
  location            = "${var.location}"
  resource_group_name = "${var.res_group_name}"
  dns_prefix          = "k8s-${terraform.workspace}"

  addon_profile {
    kube_dashboard {
      enabled = true
    }
  }

  default_node_pool {
    name            = "agentpool"
    node_count           = "${var.agent_count[terraform.workspace]}"
    vm_size         = "Standard_DS2_v2"
    os_disk_size_gb = 30
    vnet_subnet_id  = "${var.subnet_id}"
  }

  service_principal {
    client_id     = "${var.client_id}"
    client_secret = "${var.client_secret}"
  }

  network_profile {
    network_plugin = "azure"
  }

  tags = {
    Environment = "${terraform.workspace}"
  }
}