FROM public.ecr.aws/lambda/python:3.8

# install our dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN python3 -m pip install --no-cache-dir -r requirements.txt --target ${LAMBDA_TASK_ROOT}

# Copy function code and models into our /var/task
COPY ./ ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "handler.handler" ]
