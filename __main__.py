"""A local Docker Pulumi program"""
import pulumi
from pulumi_docker import Image, Container

training_script_image = Image('recommendation_model',
                            image_name='docker.io/alex/recommendation_model_image:latest',
                                build={'context' : '.',
                                       'platform' : "linux/arm64"
                                },   
                                skip_push=True)

training_script_container = Container('pulumi-test',
                                      image=training_script_image.base_image_name,
                                      # Assuming the script runs and exits
                                      command=['python', "./src/model_serving.py"],
                                      ports=[{'internal': 80, 'external': 8080}])

pulumi.export('container_id', training_script_container.id)
