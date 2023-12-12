FROM public.ecr.aws/l1p7h1f9/archesproject-fargeo:7.5.x-base-dev

ARG ARCHES_CORE_HOST_DIR
ARG ARCHES_RDM_HOST_DIR

## Setting default environment variables
ENV WEB_ROOT=/web_root
ENV APP_ROOT=${WEB_ROOT}/arches_rdm_example_project
# Root project folder
ENV ARCHES_ROOT=${WEB_ROOT}/arches
ENV ARCHES_RDM_ROOT=${WEB_ROOT}/arches-rdm

WORKDIR ${WEB_ROOT}

# Install the Arches application
# FIXME: ADD from github repository instead?
COPY ${ARCHES_CORE_HOST_DIR} ${ARCHES_ROOT}
COPY ${ARCHES_RDM_HOST_DIR} ${ARCHES_RDM_ROOT}

WORKDIR ${ARCHES_RDM_ROOT}
RUN source ../ENV/bin/activate && pip install -e . && pip uninstall arches -y

WORKDIR ${ARCHES_ROOT}
RUN source ../ENV/bin/activate && pip install -e . && pip install -r arches/install/requirements.txt && pip install -r arches/install/requirements_dev.txt

# TODO: These are required for non-dev installs, currently only depends on arches/afs
#RUN pip install -r requirements.txt

COPY /arches_rdm_example_project/docker/entrypoint.sh ${WEB_ROOT}/entrypoint.sh
RUN chmod -R 700 ${WEB_ROOT}/entrypoint.sh &&\
  dos2unix ${WEB_ROOT}/entrypoint.sh

# Set default workdir
WORKDIR ${APP_ROOT}

# # Set entrypoint
ENTRYPOINT ["../entrypoint.sh"]
CMD ["run_arches"]

# Expose port 8000
EXPOSE 8000
