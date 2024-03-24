# From Automation to AI: Exploring How Pulumi Elevates ML System Development

Author: Yi-Hsueh (Alex) Yang


To perform an initial deployment, run `pulumi up`

can also switch from using Pulumi's Docker provider to cloud-native provider, GCP, AWS and Azure are all supported.

## Overview
This project involves the development and local deployment of a movie recommendation system. The system processes data and trains a model to recommend movies to users based on their preferences. For the deployment and management of infrastructure, the project leverages Pulumi, a modern infrastructure as code (IaC) tool, alongside Docker for containerization.

## Technical Details
Infrastructure as Code with Pulumi
Pulumi is an open-source IaC tool that allows developers to define and manage infrastructure using general-purpose programming languages such as Python, JavaScript, TypeScript, and Go. In this project, Pulumi is used for orchestrating Docker containers that encapsulate the various components of the movie recommendation system, including data processing, model training, and inference.

### Key Features of Pulumi in This Project:
- Programming Language Flexibility: Pulumi’s support for familiar programming languages (Python in this case) enabled the seamless integration of infrastructure management code with the application’s logic.
- State Management: Pulumi automates the provisioning and management of resources in a desired state configuration, ensuring that the deployed infrastructure matches the defined code.
- Docker Integration: Through Pulumi’s Docker provider, Docker images are built and containers are run based on the configurations specified in the Python code. This includes setting up the environment for the recommendation model, handling dependencies, and executing the training script.

### Docker
Docker is used for containerizing the application components, ensuring consistency across different environments and simplifying deployment processes. The Docker integration with Pulumi allows for the definition, building, and running of Docker containers directly through Pulumi scripts.

#### Docker-Related Configurations:
- Dockerfile: Defines the environment for running the movie recommendation system, including the base image, dependencies, and commands to run the application.
- Pulumi Docker Provider: Manages Docker resources such as images and containers, allowing for their definition within the same codebase as the application logic.

#### Importance of Pulumi in the Project
Pulumi plays a crucial role in the project by enabling infrastructure management using the same programming language as the application code, thereby streamlining the development process. Its integration with Docker simplifies the steps needed to build and run containers, directly linking these operations with the infrastructure configuration.

## Comparison with Other Infrastructure as Code Tools
While traditional IaC tools like Terraform and AWS CloudFormation focus on declarative configurations, Pulumi distinguishes itself by:

- Programming Language Support: Offering full support for general-purpose programming languages, providing greater flexibility and the ability to use existing language features, libraries, and tools.
- Real Programming Constructs: Allowing for the use of loops, conditionals, functions, and classes in defining infrastructure, which can lead to more dynamic and reusable code.
- Unified Application and Infrastructure Management: Enabling developers to manage both application code and infrastructure in a single environment and version control system.

## Pulumi's Role in This Project
In this movie recommendation system project, Pulumi is responsible for:

- Local Infrastructure Setup: Automating the setup of local Docker containers that encapsulate the system’s components, ensuring that they are correctly configured and isolated.
- Resource Management: Handling the creation, update, and deletion of Docker resources based on the project's requirements, ensuring that the infrastructure reflects the defined state.
- Streamlining Development: Reducing the complexity associated with managing infrastructure separately from application code, thus accelerating development cycles and minimizing configuration errors.

## Conclusion
Pulumi has proven to be an integral part of the project, bringing infrastructure management capabilities into the development environment and bridging the gap between application code and infrastructure configuration. By leveraging Pulumi alongside Docker, the project achieves a high degree of automation, repeatability, and consistency in the deployment of the movie recommendation system, showcasing the potential of modern IaC practices in streamlining development workflows and enhancing productivity.