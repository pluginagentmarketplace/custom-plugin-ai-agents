---
name: kubernetes-orchestration
description: Orchestrate containerized applications with Deployments, Services, ConfigMaps, Secrets, Ingress, and Helm.
---

# Kubernetes Orchestration

Kubernetes provides container orchestration for deploying, scaling, and managing containerized applications. Master Deployments, Services, configuration management, networking with Ingress, Helm charts, and role-based access control for production-grade clusters.

## Quick Start

**Deploy an application:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-app
  labels:
    app: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: myregistry.azurecr.io/app:v1.0
        ports:
        - containerPort: 3000
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
```

**Expose with a Service:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: LoadBalancer
```

## Key Concepts

### Deployments
Control pod replicas and rolling updates:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:latest
```

### Services
Expose pods internally or externally:
- **ClusterIP**: Internal service (default)
- **NodePort**: Expose on node IP
- **LoadBalancer**: Cloud load balancer
- **ExternalName**: External DNS name

### ConfigMaps & Secrets
Store configuration and sensitive data:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: postgres.default.svc.cluster.local
  LOG_LEVEL: info
---
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  password: c2VjcmV0cGFzcw==  # base64 encoded
```

### Ingress
Route HTTP/HTTPS traffic to services:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

### RBAC (Role-Based Access Control)
Control who can do what in the cluster:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rolebinding
subjects:
- kind: ServiceAccount
  name: app-sa
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

## Common Patterns

**Pod with init containers:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  initContainers:
  - name: init-db
    image: busybox
    command: ['sh', '-c', 'until nslookup db; do echo waiting; sleep 2; done']
  containers:
  - name: app
    image: myapp:v1
```

**StatefulSet for databases:**

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

**Helm Chart for reusable deployments:**

```bash
helm create myapp
helm install myrelease ./myapp
helm upgrade myrelease ./myapp
helm rollback myrelease 1
```

## Best Practices

✅ Use namespaces to organize resources
✅ Set resource requests and limits
✅ Use health checks (livenessProbe, readinessProbe)
✅ Implement RBAC with least-privilege principle
✅ Use ConfigMaps/Secrets for configuration
✅ Use StatefulSets for stateful applications
✅ Implement network policies to restrict traffic
✅ Use Helm for package management
✅ Tag images with specific versions (not latest)
✅ Monitor with Prometheus and Grafana

## Common Pitfalls

❌ Not setting resource requests/limits
❌ Running containers as root
❌ Using latest image tags in production
❌ Not implementing health checks
❌ Storing secrets as ConfigMaps
❌ Insufficient RBAC policies
❌ Not backing up etcd (cluster data)
❌ Ignoring network policies (open by default)

## Resources

- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
