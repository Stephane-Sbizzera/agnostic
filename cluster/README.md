# Install Minikube
minikube start
# Install Kompose
kompose convert --volumes hostPath
# Apply services
sh launch.sh

