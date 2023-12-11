#! /bin/bash

APP_FOLDER=${WEB_ROOT}/${ARCHES_PROJECT_ROOT_DIRECTORY}
run_webpack() {
	echo ""
	echo "----- *** RUNNING WEBPACK DEVELOPMENT SERVER *** -----"
	echo ""
	cd ${APP_FOLDER}
    echo "Running Webpack"
	exec /bin/bash -c "source ../ENV/bin/activate && cd /web_root/arches_rdm_example_project/arches_rdm_example_project && yarn install && wait-for-it arches_rdm_example_project:80 -t 1200 && yarn start"
}

run_webpack