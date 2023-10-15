init:
	pipenv install

test:
	pipenv run python -m pytest -n 4

init-k8s:
	kubectl delete -n pulsar job test-function || exit 0
	minikube image rm python-runner:latest
	docker build . -f k8_python_runner/Dockerfile -t python-runner:latest
	minikube image load python-runner:latest

run-function-test:
	kubectl create configmap --namespace pulsar my-test-file --from-file=pytest.ini --from-file=utils.py --from-file=main.py=test_function.py -o yaml --dry-run=client | kubectl apply -f -
	kubectl delete -n pulsar job test-function || exit 0
	kubectl apply -f test-job.yaml
