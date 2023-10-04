start-docker:
	docker run -it -p 6650:6650 -p 8080:8080 --mount source=pulsardata,target=/pulsar/data --mount source=pulsarconf,target=/pulsar/conf apachepulsar/pulsar:3.1.0 bin/pulsar standalone

start-k8:
	helm repo add apache https://pulsar.apache.org/charts
	helm repo update
	kubectl create namespace pulsar
	helm install --namespace pulsar pulsar-mini apache/pulsar -f .\kubernetes\minikube.yaml
