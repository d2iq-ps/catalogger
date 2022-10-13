# Catalogger
## A simple web app to build a custom catalogue in DKP

To Deploy in kubernetes, apply the template in the install directory. This is a basic deployment and load balancer service which will work cloud hosted clusters.

```bash
kubectl create -f https://github.com/swiftsuretech/catalogger/tree/master/install
```
Once deployed, recover the endpoint with the following:

```bash
kubectl get svc -l app=catalogger -o jsonpath='{.items[0].status.loadBalancer.ingress[0].hostname}' && echo 
```

It's perhaps simpler to run on a local machine with Docker:

```bash
docker pull dswhitehouse/catalogger:latest
docker run -p 5000:5000 dswhitehouse/catalogger:latest
```
