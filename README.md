# Customer Accounts

[![CI Build](https://github.com/rautatharva706-create/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/rautatharva706-create/devops-capstone-project/actions/workflows/ci-build.yaml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-green.svg)](https://shields.io/)

This repository contains the Customer Accounts microservice project developed for the **IBM DevOps Capstone Project** which is part of the **IBM DevOps and Software Engineering Professional Certificate**.

## Project Overview

The Customer Accounts service is a RESTful microservice built with Flask, SQLAlchemy, and PostgreSQL. It implements complete CRUD operations for managing customer accounts with 95%+ test coverage, automated CI/CD pipelines, containerization with Docker, and automated deployment to Kubernetes/OpenShift.

## Project Structure

```text
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── user-story.md     <- User story issue template
│   └── workflows/
│       └── ci-build.yaml     <- GitHub Actions CI workflow
├── deploy/
│   ├── deployment.yaml       <- Kubernetes Deployment manifest
│   └── service.yaml          <- Kubernetes Service manifest
├── service/
│   ├── __init__.py           <- Application factory with Talisman & CORS
│   ├── config.py             <- Configuration settings
│   ├── models.py             <- SQLAlchemy Account data model
│   └── routes.py             <- REST API routing controllers
├── tests/
│   ├── factories.py          <- Account test factory
│   ├── test_cli_commands.py  <- CLI command tests
│   ├── test_models.py        <- Data model tests
│   └── test_routes.py        <- REST API route tests
├── Dockerfile                <- Production container configuration
├── requirements.txt          <- Python package dependencies
├── setup.cfg                 <- Tool configurations (nosetests, flake8, pylint)
└── user-story.md             <- User story template
```

## Running Tests

To run the automated test suite with coverage:
```bash
nosetests
```

## Linting

To run flake8 syntax and styling checks:
```bash
flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
```

## Author

**Atharva Raut** ([@rautatharva706-create](https://github.com/rautatharva706-create))

## License

Licensed under the Apache License, Version 2.0.
