FROM public.ecr.aws/l1p7h1f9/archesproject-fargeo:7.5.x-base-dev AS base
ENV APP_ROOT=${WEB_ROOT}/arches_rdm_example_project
WORKDIR ${WEB_ROOT}

# Install the Arches application
# FIXME: ADD from github repository instead?

# From here, run commands from ARCHES_ROOT

# COPY arches-rdm/arches_rdm/install/requirements.txt rdm-requirements.txt
COPY arches_rdm_example_project/arches_rdm_example_project/install/requirements.txt project-requirements.txt
COPY arches-rdm/ ${WEB_ROOT}/arches-rdm

RUN apt-get install nginx -y && source ENV/bin/activate && pip install -r project-requirements.txt && rm project-requirements.txt && pip install gunicorn botocore boto3 django-storages && mkdir arches_rdm_example_project && cd arches-rdm && pip install .

COPY arches_rdm_example_project/docker/production/default.conf /etc/nginx/sites-available/default

RUN  apt-get install wget -y && wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg \
  && apt-get install apt-transport-https \
  && echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-8.x.list \
  && apt-get update
RUN apt-get install sudo &&  echo 'Y' | adduser elasticsearch --disabled-password --ingroup "sudo" --gecos "First Last,RoomNumber,WorkPhone,HomePhone" && echo "elasticsearch ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers &&  su -c "sudo apt-get install elasticsearch" elasticsearch && exit 
RUN apt-get install postgresql-contrib-14 postgresql-14-postgis-3 -y && sed -i '1s/^/local all all trust\n/' /etc/postgresql/14/main/pg_hba.conf && (service postgresql start) \
  && echo "ALTER USER postgres WITH PASSWORD 'postgis';CREATE DATABASE template_postgis;CREATE EXTENSION postgis;\\q" | psql -Upostgres

COPY arches_rdm_example_project/arches_rdm_example_project ${WEB_ROOT}/arches_rdm_example_project/arches_rdm_example_project
COPY arches_rdm_example_project/manage.py ${WEB_ROOT}/arches_rdm_example_project/manage.py
WORKDIR ${APP_ROOT} 
RUN chown elasticsearch:elasticsearch /etc/elasticsearch -R && \
  chown elasticsearch:elasticsearch /usr/share/elasticsearch -R && \
  chown elasticsearch:elasticsearch /etc/default/elasticsearch && \
  cd arches_rdm_example_project && yarn install

RUN ESPASSWORD='$(echo "y" | sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic | grep "New value:" | cut -d " " -f 3)' && export ES_JAVA_OPTS="-Xmx1g" && \
  sed -i 's/xpack.security.enabled: true/xpack.security.enabled: false/g' /etc/elasticsearch/elasticsearch.yml && \
  sed -i 's/xpack.security.enrollment.enabled: true/xpack.security.enrollment.enabled: false/g' /etc/elasticsearch/elasticsearch.yml && \
  (su -c "/usr/share/elasticsearch/bin/elasticsearch" elasticsearch>/dev/null 2>&1&) && \
  (service postgresql start) && sleep 30 && source ../ENV/bin/activate && (python3 manage.py setup_db --force) 

RUN source ../ENV/bin/activate && service postgresql start && \
  (/etc/init.d/nginx start&) && (gunicorn arches_rdm_example_project.wsgi&) && \
  cd arches_rdm_example_project && yarn run build_development && cd ../ && python3 manage.py collectstatic


FROM ubuntu:22.04 as final 
ENV DEBIAN_FRONTEND=noninteractive
ENV WEB_ROOT=/web_root
ENV APP_ROOT=${WEB_ROOT}/arches_rdm_example_project
COPY --from=base /var/www/media /var/www/media
COPY --from=base /web_root/ENV /web_root/ENV

RUN chgrp www-data /var/www/media -R
RUN apt-get update && apt-get install -y make software-properties-common && apt-get install -y ca-certificates curl gnupg nginx vim && apt-add-repository ppa:deadsnakes/ppa && apt-get update
# Install packages required to run Arches
# Note that the ubuntu/debian package for libgdal1-dev pulls in libgdal1i, which is built
# with everything enabled, and so, it has a huge amount of dependancies (everything that GDAL
# support, directly and indirectly pulling in mysql-common, odbc, jp2, perl! ... )
# a minimised build of GDAL could remove several hundred MB from the container layer.
RUN set -ex \
  && RUN_DEPS=" \
  build-essential \
  mime-support \
  libgdal-dev \
  python3.11 \ 
  python3.11-distutils \
  python3.11-venv \
  postgresql-client-14 \
  dos2unix \
  " \
  && apt-get install -y --no-install-recommends curl \
  && apt-get install apt-transport-https \
  && apt-get update -y \
  && apt-get install -y $RUN_DEPS --no-install-recommends


RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py \
  && rm -rf /root/.cache/pip/* 

COPY arches-rdm/ ${WEB_ROOT}/arches-rdm

COPY arches_rdm_example_project/docker/entrypoint.sh ${WEB_ROOT}/entrypoint.sh
RUN chmod -R 700 ${WEB_ROOT}/entrypoint.sh &&\
  dos2unix ${WEB_ROOT}/entrypoint.sh

COPY arches_rdm_example_project/docker/production/default.conf /etc/nginx/sites-available/default
COPY arches_rdm_example_project/ ${WEB_ROOT}/arches_rdm_example_project
WORKDIR ${APP_ROOT}

ENTRYPOINT ["../entrypoint.sh"]
CMD ["run_arches_production"]