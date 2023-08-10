# Technical Proposal: Multi-environments Database Design


<!-- toc -->
- [Introduction](#introduction)
    - [Summary](#summary)
    - [Goals](#goals)
    - [Non-Goals](#non-goals)
- [Proposal](#proposal)
    - [Assumptions](#assumptions)
    - [Detailed Solution](#solution)
    - [Risks and Mitigations](#risks-and-mitigations)
<!-- /toc -->

## Introduction
### Summary
The objective of this proposal is to produce a design for the setup of database infrastructure in the context of microservices deployed in different environments namely test and production environments for now.

### Goals
The proposal aims to achieve the following goals:
- come up with a Multi-environments Database infrastructure design considering the following points:
    - Database deployment
    - Database infrastructure architecture
    - Database multi-environment setup in the context of microservices architecture
    - Access management and security

### Non-Goals
To make our scope of work clear, in this proposal we are not aiming to:
- Describe how applications communicate with each other/database from a networking perspective.
- Outline the internal design of the database (in terms of schema).

## Proposal
### Assumptions
Before diving deep into the design of the architecture, some assumptions should be made to clarify our decision process which gives better insights for reviewers:
- Since microservices are deployed on a Kubernetes cluster, and it was not mentioned whether it is on-premises or not, I would assume that we are deploying services on the AWS-managed Kubernetes service: EKS.
- We do not have severe cost limitations, i.e. we have the freedom to choose whatever option we want as long we meet our functional and non-functional requirements.
- We are expecting 100k requests per second in the production environment and less than 1k requests in the test environment. (These numbers are just an assumption, and we want to just to outline the fact that we are expecting more load on the production environment).
- The test environment is used for e2e and integration tests only. Other kinds of tests such as load testing, and stress testing are not taken into consideration for this environment.
- We consider the test and production environments identical as in having the same functionality but they can have different infrastructure/scaling.

### Detailed Solution
#### Database Deployment
Considering the fact that our services are deployed on top of EKS, for the following reasons it makes sense to deploy the database on top of AWS, specifically on top of RDS using the Aurora serverless:

- **Consistency:** Managing all of our infrastructure in one cloud provider, AWS in our use case, is beneficial for the DevOps team to keep our infrastructure well-managed. Added to this, AWS provides a great integration between EKS and other AWS services using operators, such as the AWS IAM operator, that can be used for access management.

- **Development Efficiency:** Achieving our non-functional requirements, in terms of scalability, reliability, availability, automated backups and restore, and OS patches and updates, would require a lot of configuration overhead and hustle. Therefore, delegating the management of the database to AWS would save a lot in terms of engineering efforts, which give us the option to focus on other aspects.

The choice of the Aurora engine with Postgres compatibility instead of the Postgres engine is justified by the fact that the Aurora engine has a better throughput according to [the following benchmark](https://severalnines.com/blog/benchmarking-managed-postgresql-cloud-solutions-part-two-amazon-rds), and AWS generally is recommending using it.

Finally, to optimize the costs of the database, we opted for a serverless option of Aurora that can **save us up to 90%** of costs.

The choice of database deployment remains the same for both environments.

#### Database Infrastructure Architecture
- For the test environment, we are not expecting a great amount of traffic on the database followed by the fact that data loss is not an issue in this environment as we can always reproduce the same data using some fake data. That said, deploying a single server of the database should be a good option that satisfies our requirements, keeping costs at a minimal level.

- For the production environment, requires a different approach from the test environment. We are expecting a high load on the database during the day, while also the data loss is critical in this environment since we are using real business data, not fake one. As a result, achieving a good level of scalability, reliability, and availability is crucial and should be taken into consideration in our use case. Deploying a cluster of RDS should respond well to our requirements. We can deploy up to 15 replicas per cluster while ensuring data synchronization. The load should be distributed amongst these replicas while having a primary database serving write requests. This is how we can ensure the scalability of the database. To ensure the reliability and availability of the database, we can use the replication mechanism cross region/AZ to mitigate potential issues that can happen in AWS infrastructures. Finally, it is worth mentioning that storage also can scale accordingly in AWS RDS Aurora.

#### Database Multi-enviornments/Multi-applications Setup
For a good separation between environments, we'll opt to deploy a database in each environment.

- In the test environment, we can link all microservices with the same database to optimize costs, assuming that we won't run into potential conflicts on the application level if these microservices share the same database server.

- In the production environment, following the microservices architecture best practices, it is usually recommended to deploy a database for each microservice to ensure a good separation and independence in these microservices. However, we can always adapt depending on the context of the project. We can have a single cluster for all of the microservices if, at an early stage, we want to minimize costs and the number of resources to manage.

#### Database Access Management & Security
- To isolate the database, we can opt to deploy it in a private subnet of the same VPC as the EKS cluster, which will result in denying access from the public internet to the database and allowing access only from pods inside the EKS cluster.

- To improve the security of the database, we can set up a security group that serves as a firewall to inhibit malicious access. this security group would only allow access from the EKS cluster.

- Access management can be easily implemented through AWS IAM. A possible solution for developers' access to the services in the AWS account, we can create IAM users for each member of the team. Each IAM user is part of an IAM group that has a policy denying write access and allowing read access to services deployed in the production environment, and allowing read and write access to services deployed in the test environment. Database authentication can be implemented with the IAM authentication option in the RDS, allowing each application to access the database using its specific credentials and roles relying on the least-privilege security principle. These IAM roles can be used by pods as service accounts mounted to the pod (in the service account annotations we put the role arn).

- for further separation between environments, we can opt for a multi-account environment, where each environment is deployed on a separate AWS account.

### Risks and mitigations
- If we have a constraint on where the data should be stored, we can sometimes be obliged to shift our work to on-premises. In this use case, we need to implement all of the techniques that were discussed during the proposal by ourselves.

- If the test environment is a staging environment or an environment that is used for load testing it is preferable to make the infrastructure similar to the production environment, we should preferably use the same architecture for the database which can increase the costs coming from the database.

- Having a cost limitation can be a problem for us in some use cases that should be mitigated by reducing the number of features used in the RDS. e.g.: removing replication, reducing the number of replicas, etc...

