## Dotnet Core Sample App
A .Net Core sample application is based on dotnet 7.0 with Promethus nuget package for exposing the app metrics.

Prerequisite:
 - Make sure .Net Core 7.0 is installed in your environment.
 - Use Visual Studio Code to build and run this project.

### Building the project and creating the docker image:

1. Checkout the project and goto DotnetCoreSample directory.
2. Run `docker build .` to build the project.
3. List docker images `docker images`.
4. Tag the docker image `docker tag <image-ID> <docker-hub-repository>/dotnet-core-app:v1`.
5. Push the image to docker hub `docker push  <docker-hub-repository>/dotnet-core-app:v1`.

### Deploying the docker image in Kubernetes environment:

You can deploy the docker image either using `kubectl run` command or `kubectl deploy` the `yaml` file.

#### Using `kubectl run` command:

1. Create a env variable `override`:
	$override = '{"apiVersion": "v1", "spec": {"nodeSelector": { "kubernetes.io/os": "windows" }}}' | ConvertTo-Json

2. Deploy a pod:
	kubectl run dotnet-test --image gangadharaswamy/dotnet-core-app:v1 --port 8080 --overrides=$override

3. Expose the pod over a service:
	kubectl expose pod dotnet-test --port=8080 --name=dotnet-test-svc --type="LoadBalancer" --target-port=80


#### Using `yaml` file:

1. Download the [yaml](<path>) file.

2. Update the image in yaml file.

3. Deploy the sample app using yaml file.
	`kubectl apply -f sample-app.yaml`
