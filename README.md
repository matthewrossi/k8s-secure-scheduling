# k8s-secure-scheduling

## Rationale

Scheduling pods on separate physical nodes is a crucial strategy to isolate
workloads with incompatible security requirements. In Kubernetes, this is
enforced using metadata such as node selectors, affinity rules, and topology
spread constraints, all manually defined by developers at resource creation.
The aforementioned process is complex and prone to errors, frequently resulting
in misconfigurations that expose systems to data breaches and regulatory
violations.

This repository presents an approach to constrain scheduling using policies
defined once at the cluster level and automatically evaluated by Kubernetes
during each workload deployment. The advantages are (i) automatic rejection of
uncompliant resource creation requests, (ii) streamlined support for executing
multi-tenant workloads, and (iii) secure scheduling and deployment of workloads
based on security requirements. To implement this solution, we integrate the
native Kubernetes node-filtering capabilities with OPA Gatekeeper for policy
enforcement. Experimets demonstrate reliable enforcement of common corporate
governance policies with minimal overhead and significant performance advantage
over isolation achieved solely through sandboxing.

## References

<a id="1">[1]</a>
M. Rossi, M. Beretta, D. Facchinetti, S. Paraboschi.
POSTER: Policy-driven security-aware scheduling in Kubernetes.
In _Proceeding of the 16th IEEE International Conference on Cloud Computing Technology and Science (CLOUDCOM)_, Shenzhen, China, November 14-16, 2025. ([Available here](https://cs.unibg.it/seclab-papers/2025/ASIACCS/poster-security-aware-scheduling.pdf)).

<a id="2">[2]</a>
M. Rossi, M. Beretta, D. Facchinetti, S. Paraboschi.
Secure Kubernetes Workload Deployment with Automated Enforcement of Cluster-Defined Policies.
In _Proceeding of the 20th ACM ASIA Conference on Computer and Communications Security (ASIACCS)_, Hanoi, Vietnam, August 25-29, 2025. ([Available here](https://cs.unibg.it/seclab-papers/2025/CLOUDCOM/secure-scheduling.pdf)).
