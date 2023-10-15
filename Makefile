start-docker:
	docker run -it -p 6650:6650 -p 8080:8080 --mount source=pulsardata,target=/pulsar/data --mount source=pulsarconf,target=/pulsar/conf apachepulsar/pulsar:3.1.0 bin/pulsar standalone

start-k8:
	helm repo add apache https://pulsar.apache.org/charts
	helm repo update
	minikube start
	kubectl create namespace pulsar || echo "Already created"
	helm upgrade --install --namespace pulsar pulsar-mini apache/pulsar -f .\kubernetes\minikube.yaml

test-k8:
	kubectl exec -it -n pulsar pulsar-mini-toolset-0 -- bin/pulsar-admin tenants list

expose-locally:
	minikube service pulsar-mini-proxy -n pulsar --url
