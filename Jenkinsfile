pipeline {
    agent { label 'worker' }
    options {
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        REPO_NAME = sh(returnStdout: true, script: 'basename `git remote get-url origin` .git').trim()
        VERSION = sh(returnStdout: true, script: 'uv version --short').trim()
        LATEST_AUTHOR = sh(returnStdout: true, script: 'git show -s --pretty=%an').trim()
        LATEST_COMMIT_ID = sh(returnStdout: true, script: 'git describe --tags --long  --always').trim()

        SNAPSHOT_BRANCH_REGEX = /(^main$)/
        RELEASE_REGEX = /^([0-9]+(\.[0-9]+)*)(-(RC|beta-|alpha-)[0-9]+)?$/
        RELEASE_DEPLOY = false
        SNAPSHOT_DEPLOY = false
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo REPO_NAME
                    echo LATEST_AUTHOR
                    echo LATEST_COMMIT_ID

                    echo env.BRANCH_NAME
                    echo env.BUILD_NUMBER
                    echo env.TAG_NAME

                    if (!(VERSION ==~ RELEASE_REGEX || VERSION ==~ /.*-SNAPSHOT$/)) {
                        echo 'Version:'
                        echo VERSION
                        error 'The version declaration is invalid. It is neither a release nor a snapshot.'
                    }
                }
                script {
                    sh 'uv sync --all-extras --locked --no-editable'
                }
            }
            post {
                failure {
                  rocket_buildfail()
                }
            }
        }

        stage('Test') {
            environment {
                VIRTUAL_ENV="${WORKSPACE}/.venv"
                PATH="${VIRTUAL_ENV}/bin:${PATH}"
            }
            steps {
                script {
                    // run pytest
                    sh 'pytest --cov=pytest_approval --cov-report=xml tests'
                    sh 'pytest --markdown-docs -m markdown-docs README.md'
                    sh 'pytest -n auto'  // test if library works with pytest-xdist
                    sh 'uv run --all-extras --python 3.11 pytest'  // test if library works with pytest-xdist
                    // run static analysis with sonar-scanner
                    def scannerHome = tool 'SonarScanner 4'
                    withSonarQubeEnv('sonarcloud GIScience/ohsome') {
                        SONAR_CLI_PARAMETER =
                            "-Dsonar.python.coverage.reportPaths=${WORKSPACE}/coverage.xml " +
                            "-Dsonar.projectVersion=${VERSION}"
                        if (env.CHANGE_ID) {
                            SONAR_CLI_PARAMETER += ' ' +
                                "-Dsonar.pullrequest.key=${env.CHANGE_ID} " +
                                "-Dsonar.pullrequest.branch=${env.CHANGE_BRANCH} " +
                                "-Dsonar.pullrequest.base=${env.CHANGE_TARGET}"
                        } else {
                            SONAR_CLI_PARAMETER += ' ' +
                                "-Dsonar.branch.name=${env.BRANCH_NAME}"
                        }
                        sh "${scannerHome}/bin/sonar-scanner " + SONAR_CLI_PARAMETER
                    }
                    // run other static code analysis
                    sh 'ruff format --check --diff .'
                    sh 'ruff check .'
                }
            }
            post {
                failure {
                  rocket_testfail()
                }
            }
        }

        stage('Build and Deploy Package') {
            when {
                expression {
                    return VERSION ==~ RELEASE_REGEX && env.TAG_NAME ==~ RELEASE_REGEX
                }
            }
            steps {
                script {
                    sh 'uv build'
                    withCredentials([string(credentialsId: 'PyPI-API-Token', variable: 'UV_PUBLISH_TOKEN')]) {
                        sh 'uv publish'
                    }
                }
            }
        }

        stage('Wrapping Up') {
            steps {
                encourage()
                status_change()
            }
        }
    }
}
