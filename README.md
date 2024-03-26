# From Automation to AI: Exploring How Pulumi Elevates ML System Development

Author: Yi-Hsueh (Alex) Yang

**View on [Medium](https://medium.com/@alex0990370/from-automation-to-ai-exploring-how-pulumi-elevates-ml-system-development-3d37444906aa) for better visual**

*This article is part of the coursework of the course Machine Learning in Production (17–445/17–645/17–745) / AI Engineering (11–695) provided by CMU in 2024 spring. The data provided for the scenario discussed below is also gathered from the Kafka broker used for the group project in the course.*


## Introduction to Pulumi
In the rapidly evolving landscape of cloud computing and infrastructure management, Pulumi emerges as a groundbreaking tool, fundamentally transforming how developers create, deploy, and manage infrastructure across any cloud. Pulumi stands out by allowing developers to use familiar general-purpose programming languages such as JavaScript, TypeScript, Python, Go, and .NET instead of relying on domain-specific languages. This approach not only democratizes infrastructure management by making it accessible to a broader range of developers but also enhances productivity, reusability, and collaboration within teams.

Pulumi's design philosophy centers around providing a unified infrastructure as code (IaC) platform that seamlessly integrates with existing development workflows and tools. It empowers developers to define cloud resources using code, which can then be versioned, reused, and shared, much like application code. By treating infrastructure as a first-class citizen of the development process, Pulumi bridges the gap between application development and operations, fostering a more DevOps-centric approach.

## Pulumi vs. Traditional IaC Tools: A Brief Comparison with Terraform
While Terraform has long been the go-to IaC tool for many developers, Pulumi introduces several innovations that make it particularly appealing, especially for complex deployments like Machine Learning (ML) systems. The primary differentiator between Pulumi and Terraform lies in their approach to defining infrastructure:

- Programming Language Flexibility: Terraform uses a custom domain-specific language (DSL) called HCL (HashiCorp Configuration Language), which, while powerful, requires users to learn a new syntax and has limitations in terms of logic and conditionals. Pulumi, on the other hand, allows the use of general-purpose programming languages, offering greater flexibility, the ability to use existing libraries, and the power to apply familiar patterns and practices.
- State Management: Both Pulumi and Terraform manage infrastructure state, but Pulumi's approach to state management is more integrated with the developer's workflow, supporting a wider range of backend options for state storage and offering more robust collaboration features.
- Ecosystem and Community: Terraform benefits from a large ecosystem and community, with a vast library of providers and modules. Pulumi is rapidly growing its ecosystem, focusing on deep integration with cloud-native technologies, container orchestration systems like Kubernetes, and now, machine learning workflows.
- Unified Application and Infrastructure Management: Enabling developers to manage both application code and infrastructure in a single environment and version control system.

---

Now, Let’s dive into some implementations and test the capability of Pulumi!

## Example Implementation
To illatrate and test the capability of Pulumi, we tried to implement Pulumi into a simple scenario where we deploy a **movie recommendation system** locally. The system processes data and trains a model to recommend movies to users based on their preferences. For the deployment and management of infrastructure, the project leverages Pulumi, alongside Docker for containerization.

In this demonstration, Pulumi is used for orchestrating Docker containers that encapsulate the various components of the movie recommendation system, including data processing, model training, and inference.

Creating and deploying a movie recommendation system locally using Docker and Pulumi involves several steps, from setting up the project environment to defining the infrastructure with Pulumi and running the application. The whole project tryouts can be found [here](https://github.com/Yi-Hsueh-Yang/Pulumi_tryouts.git). Or, you can choose to create your own following the detailed step-by-step guide:

### Step 1: Set Up the Project Directory
1. **Create a Project Directory:** This will contain all your project files, including application code, Dockerfile, Pulumi scripts, and virtual environment.

	```mkdir movie_recommendation``` <br>
	```cd movie_recommendation```

2. **Create a Virtual Environment** (putting the venv in a deployment folder is for the ease of deployment with Pulumi later on)

	```python -m deployment/venv venv```
	```source deployment/venv/bin/activate  # On Windows use 	`venv\Scripts\activate\````

3. **Add a requirements.txt File:** Include all necessary Python dependencies.

	`pulumi>=3.0.0 
	pulumi_docker==4.5.2
	pandas==2.0.3
	scikit-learn==1.3.2
	numpy==1.26`

4. **Install Dependencies:**

	```pip install -r requirements.txt```
	
### Step 2: Initialize the Pulumi Project
1. **Create a New Pulumi Project**, then follow the prompts to set up the project. You can choose to save your project’s state locally or on the Pulumi service.
pulumi new python
2. **Configure the Project**: tweak the `Pulumi.yaml` to your specific need, we are only showing the basic functionality of it, so nothing fancy here.

	`name: movie_recommendation
	runtime:
	  name: python
	  options:
	    virtualenv: venv
	description: A minimal local Docker Python Pulumi program`
	
### Step 3: Write the Application Code
* Develop the Application: Write the code for your movie recommendation system or you can simply clone the written scripts for this demo. Remember to include scripts for data preprocessing, model training, and inferencing if building your recommendation system.
> Disclaimer:
> 
> Since the data comes from a private Kafka broker used in the course, I found that it will be more convenient to reproduce my result if the data is static, hence ratings.json found in /src is created.
> 
> Modeling and Accuracy are not the main focus here, therefore, you may find the process of training not robust enough or wonky results from the inference. All in all, it only needs to serve as a response machine and returns some movie_id for recommendation, then we are good to go!

* Dockerfile: Create a Dockerfile in the project root to specify how to containerize the application.

	`FROM python:3.9
	WORKDIR /app
	COPY . /app
	RUN pip install --no-cache-dir -r requirements.txt --verbose
	CMD ["python", "./src/model_serving.py"]`

### Step 4: Define the Infrastructure with Pulumi
This is the most crucial part where IaC comes into practice. In `__main__.py,` define the Docker infrastructure needed to run the application:


	"""A local Docker Pulumi program"""
	import pulumi
	from pulumi_docker import Image, Container
	
	training_script_image = Image('recommendation_model',
	                            image_name='docker.io/yourname/recommendation_model_image:latest',
	                                build={'context' : '.',
	                                       'platform' : "linux/arm64"
	                                },   
	                                skip_push=True)
	
	training_script_container = Container('pulumi-test',
	                                      image=training_script_image.base_image_name,
	                                      # Assuming the script runs and exits
	                                      command=['python', "./src/model_serving.py"],
	                                      ports=[{'internal': 80, 'external': 8080}]))
	
	pulumi.export('container_id', training_script_container.id)
	
This snippet is creating aPulumi program that uses the pulumi_docker package to define and manage Docker resources. The imports set up the script to define Docker resources using Pulumi’s infrastructure as code capabilities. The first partImage represents a Docker image resource in Pulumi.

* `recommendation_model` is the name given to this Pulumi resource.
* `image_name` specifies the name and tag of the Docker image. In this case, it's `docker.io/yourname/recommendation_model_image:latest`. (It’s recommended to specify the Docker Hub username or organization under which the image is hosted, e.g. `docker.io/yourname` , for Pulumi to find the Docker image easily.
* `build` is a dictionary that defines how to build this Docker image. `context` is set to `.`, indicating the current directory as the build context. `platform` specifies the target platform for the build, here set to `linux/arm64`. (If you are a Windows User, remember to change it to your corresponding architecture)
* `skip_push` is set to `True`, indicating that the image should not be pushed to a Docker registry after being built.

The second part Containerrepresents a Docker container resource in Pulumi.

* `pulumi-test` is the name given to this Pulumi resource.
* `image` specifies the image to use for the container. `training_script_image.base_image_name` refers to the Docker image defined earlier.
* `command` is an array specifying the command to run inside the container. Here, it runs a Python script located at `./src/model_serving.py`.

The third part exports the container’s ID as a stack output, making it accessible outside of Pulumi for further reference or use.

With only these three parts, Pulumi has demonstrated plenty of its helpful features:

1. Language Familiarity and Flexibility: Pulumi allows us to define infrastructure using general-purpose programming languages (e.g., Python, JavaScript, TypeScript), making it accessible to developers who might not be familiar with domain-specific languages (DSLs) used by other IaC tools.
2. Integrated Software Development Practices: Since Pulumi uses programming languages, it integrates well with existing software development practices(can be pushed and viewed in GitHub), such as version control, code review, and continuous integration/continuous deployment (CI/CD) pipelines.
3. Dynamic Infrastructure Management: Pulumi enables dynamic generation of infrastructure configuration, which can be based on external inputs, logic, and conditions. This allows for more flexible and customizable infrastructure setups.

### Step 5: Deploy Your Application
1. **Create a dev stack:** Every Pulumi program is deployed to a stack. A stack is an isolated, independently [configurable](https://www.pulumi.com/docs/concepts/config/) instance of a Pulumi program. It is a good practice to use stacks for different stages of product development. For more info on Pulumi Stack, reference [here](https://github.com/Yi-Hsueh-Yang/Pulumi_tryouts/tree/main).
`pulumi stack init staging`

Show all existing stack:

`pulumi stack ls`

Select working stack: use `up` and `down` on the keyboard to navigate to the desired stack.

`pulumi stack select dev`

2. Run `pulumi up` to propose changes on infrastructure:

`pulumi up`

`pulumi up` provides a preview that details what will happen when the command executes. This preview shows you resources that will be created, updated, or deleted based on the current state of your infrastructure as defined in your code versus the actual state in your target environment. Pulumi maintains a state file that tracks the resources in your stack. Running `pulumi up` updates this state to reflect the actual state of your infrastructure after the changes. Also, when you modify configuration values for your stack (using `pulumi config set`), `pulumi up` applies these configuration changes to your resources.

### Step 6: Iterate and Update
* As the development of the application goes on, you can run `pulumi up` again to apply any changes you make to your code, Dockerfile, or Pulumi infrastructure definitions.
* Due to frequent configuration changes may sometimes confuse Pulumi, when it does happen, try to refresh the stack, `pulumi refresh`, to make the changes.

---

Pulumi stands out for its seamless integration capabilities, particularly with GitHub, enabling developers to streamline their deployment workflows effortlessly. By linking a repository in GitHub with Pulumi, developers can set up automated deployments that trigger with every new push to the repository. This feature not only enhances productivity but also ensures that the deployment process is tightly integrated with version control, allowing for continuous integration and continuous deployment (CI/CD) practices to be implemented more effectively. Through this integration, Pulumi offers a robust solution for managing infrastructure as code, making it easier for teams to maintain consistency, reduce errors, and speed up the release cycles in their development processes.

### Docker and Docker-Related Configurations:
Docker is used for containerizing the application components, ensuring consistency across different environments and simplifying deployment processes. The Docker integration with Pulumi allows for the definition, building, and running of Docker containers directly through Pulumi scripts.

- Dockerfile: Defines the environment for running the movie recommendation system, including the base image, dependencies, and commands to run the application.
- Pulumi Docker Provider: Manages Docker resources such as images and containers, allowing for their definition within the same codebase as the application logic.

### Importance of Pulumi in the above tryout
Pulumi plays a crucial role in this implementation by enabling infrastructure management using the same programming language as the application code, thereby streamlining the development process. It also manages resources well by handling the creation, update, and deletion of Docker resources based on the project’s requirements, ensuring that the infrastructure reflects the defined state. Its integration with Docker simplifies the steps needed to build and run containers, directly linking these operations with the infrastructure configuration.

## What else can Pulumi do?

Beyond the local deployment of machine learning models that we are doing here, Pulumi offers a vast array of functionalities for more sophisticated deployment scenarios, catering to the diverse needs of modern ML architectures. Pulumi also supports major cloud providers like Google Cloud Platform (GCP), Amazon Web Services (AWS), and Microsoft Azure for seamless integration and deployment of cloud resources. For instance, we can configure the data collecting process from Kafka and then store the data in cloud databases such as AWS RDS, Azure SQL Database, or Google Cloud SQL for easy provision and manage. We can therefore ensure our ML models have the necessary data storage and retrieval capabilities with robust security and scalability.

Additionally, Pulumi facilitates the deployment of ML models in cloud environments by managing compute resources like AWS EC2 instances, Azure VMs, or Google Compute Engine instances, as well as serverless platforms like AWS Lambda, Azure Functions, and Google Cloud Functions. This flexibility allows for a variety of deployment strategies, from traditional VM-based applications to modern containerized services using Kubernetes or managed container services like AWS ECS, Azure Container Instances, or Google Kubernetes Engine.


## Conclusion
Pulumi has proven to be an integral part of the project, bringing infrastructure management capabilities into the development environment and bridging the gap between application code and infrastructure configuration. By leveraging Pulumi alongside Docker, our above tryout achieves a high degree of automation, repeatability, and consistency in the deployment of the movie recommendation system, showcasing the potential of modern IaC practices in streamlining development workflows and enhancing productivity.

Thanks to Pulumi’s infrastructure as code (IaC) approach which simplifies the process of setting up complex networking, security, and monitoring configurations, ensuring our ML deployments are not only performant and reliable but also secure and compliant with industry standards. By leveraging Pulumi’s comprehensive ecosystem, developers and data scientists can focus more on optimizing their ML models and less on the underlying infrastructure, accelerating the path from development to production.