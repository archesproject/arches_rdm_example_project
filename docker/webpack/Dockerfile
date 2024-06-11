FROM public.ecr.aws/l1p7h1f9/archesproject-fargeo:7.5.x-base-dev
ENV WEB_ROOT=/web_root
ENV ARCHES_ROOT=${WEB_ROOT}/arches
ENV APP_ROOT=${WEB_ROOT}/arches_rdm_example_project
ENV ARCHES_LINGO_ROOT=${WEB_ROOT}/arches-lingo
ENV NODE_MAJOR=20
ENV DEBIAN_FRONTEND=noninteractive

COPY ./arches ${ARCHES_ROOT}
COPY ../arches-lingo ${ARCHES_LINGO_ROOT}
RUN apt update && apt install wait-for-it

WORKDIR ${ARCHES_LINGO_ROOT}
RUN apt-get update && apt-get install gettext -y && source ../ENV/bin/activate && pip install -e . && pip uninstall arches -y

WORKDIR ${ARCHES_ROOT}
RUN source ../ENV/bin/activate && pip install -e . && pip install -r arches/install/requirements.txt && pip install -r arches/install/requirements_dev.txt

COPY /arches_rdm_example_project/docker/entrypoint.sh ${WEB_ROOT}/entrypoint.sh
RUN chmod -R 700 ${WEB_ROOT}/entrypoint.sh
WORKDIR ${WEB_ROOT}
ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["run_webpack"]
EXPOSE 8021
