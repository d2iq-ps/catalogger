# Custom Catalogue Applications

Your custom catalogue has been built and is ready to deploy to DKP. Set the relevant namespace for either workspace or project, depending on the scope you chose, as an environmental variable:

```bash
export NAMESPACE=[your_namespace]
````

Copy and past the following into the terminal to deploy the catoalogue:

```bash
kubectl apply -f - <<EOF
apiVersion: source.toolkit.fluxcd.io/v1beta1
kind: GitRepository
metadata:
  name: {{ repo_name | default('[Your Repo Name]')}}
  namespace: ${NAMESPACE}
  labels:
    kommander.d2iq.io/gitapps-gitrepository-type: catalog
    kommander.d2iq.io/gitrepository-type: catalog
spec:
  interval: 1m0s
  ref:
    branch: master
  timeout: 20s
  url: {{ git_url | default('[Your Github Repo URL]')}}
EOF
```