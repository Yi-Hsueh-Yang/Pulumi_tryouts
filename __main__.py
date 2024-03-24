"""A local Docker Pulumi program"""
import pulumi
from pulumi_docker import Image, Container

training_script_image = Image('recommendation_model',
                            image_name='docker.io/alex/recommendation_model_image:latest',
                                build={'context' : '.'},
                                skip_push=True)

training_script_container = Container('pulumi-test',
                                      image=training_script_image.base_image_name,
                                      # Assuming the script runs and exits
                                      command=['python', "./src/model_serving.py"])

pulumi.export('48104a77fa88148b34622991fdff9f42129262103466a7e3f708560214933ab5', training_script_container.id)
# container_id