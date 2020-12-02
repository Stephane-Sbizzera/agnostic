variable "appId" {
  description = "Azure Kubernetes Service Cluster service principal"
}

variable "password" {
  description = "Azure Kubernetes Service Cluster password"
}
variable location {
    default = "Central US"
}
variable resource_group_name {
    default = "azure-k8stest"
}