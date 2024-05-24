# Doug's Openverse Test Framework

## Project Introduction

This automation framework represents the foundations of a test harness that I believe to be robust, extensible, and maintainable. I am a proponent of Behavior Driven Development, therefore I chose to use BDD tooling as a part of this project.

## Tools Overview

1. Python 3.12 ([www.python.org](https://www.python.org/downloads/release/python-3123/))

    Python is my current language of choice. It is a flexible language with excellent readability. It is also a preferred language in the QA/SDET community. This should make on-boarding new SDETs to this project more easy.

    I chose to be on the cutting edge of Python releases (3.12) with this project due to the lack of existing environmental constraints. Were I in a situation where Python was already in use, I would have prioritized using the version supported by Development, DevOps, and/or other QA Engineers. I expect that this most likely would have been 3.10 or 3.11. I consider anything >= 3.9 to be an acceptable choice.

2. Poetry (https://python-poetry.org/docs/#installation)

    Management of dependencies, up to and including Python versions, is a common problem in Python projects. There are several tools in active development that attempt to resolve this problem. ([This](https://packaging.python.org/en/latest/tutorials/managing-dependencies/) article has an overview of the situation and some tools.) I looked at a small number of these tools (Pipenv, PDM, Hatch, and Poetry) for use in this project. I decided to use Poetry for its features as well as its maturity and stability.

    Poetry is responsible for managing the PyProject.toml and the  '.poetry.lock' file. PyProject.toml is a recent standard for managing project dependencies. The '.poetry.lock' file is a record of the versions of libraries used in the project. These two files will allow someone deploying the project to their system for the first time to easily setup a Python Virtual Environment and install the correct versions of the libraries used in the project.

3. Pytest

    Pytest is a robust, mature, and popular tool for testing Python code. It is most often used for Unit Tests in Python projects, but it can be used as a test runner for most types of automated tests.

    I chose Pytest because I am familiar with the tool and was already using it for a personal project. While personal preference was a significant criteria for my choice, I also considered what might integrate well with an existing Development or SDET team. It is likely that any existing Python project would be using Pytest for Unit Testing or other automation. So, I thought it to be a sensible choice.

4. Pytest-BDD

    Pytest-BDD is a third party plugin for Pytest. It provides the ability to create Cucumber-style BDD automation tests in Python using Pytest as the test runner. It is a mature tool with good community support.

    There is another tool, Behave, that may have been a better choice to get up and running more quickly with this project. This tool did require a small bit of research to get Pytest to properly execute the BDD tests. Behave, on the other hand, is a complete platform that includes its own test runner. This proved to be a small hurdle and I don't regret the choice even if it did cost me some time.

5. PyYAML library

    YAML ([yaml.org](https://yaml.org/)) is a very readable markup language. It is used by many projects, including Kubernetes and CircleCI, as the language for all configuration files. Therefore, it is well understood by DevOps Engineers and should be familiar to most Software Engineers and QA Engineers.

    I chose to use this for my configuration files due to its prevalence and also because it is a robust and well supported community standard. I could have used the TOML language, since that is an up-and-coming standard in the Python community which has some support in the Python Standard Library. However, YAML seemed to be the more mature standard and therefore a better choice.

6. Requests library

    When working with REST APIs in Python this library is the standard choice. It is a mature library that is well supported within the Python community. It was the obvious choice for this project.

7. Postman

    In the 'docs' directory of the project is a YAML file that was downloaded from the Openverse API site. I used this file to create the Postman collection file that is in the same directory.

    Postman is my preferred tool for manual API testing. It is also a valuable tool for automation test development as it allows the automation developer to work with actual data on a live system. Using this tool during development made the process less error prone. 

## Framework Setup and Use

Using this framework should be as simple as:

1. Installing Python 3.12
2. Installing the Poetry tool
3. Pulling this Github repository
4. Running the Poetry tool within the repo.

The first time that Poetry is run it should find PyProject.toml and '.poetry.lock'. At that point the tool should create a VENV for the project and install the libraries into the VENV.

Once that is done the following command should execute the tests:

    poetry run pytest

Use this command to execute just a single Feature:

    poetry run pytest -k "audio"

The tests in the framework are divided into two parts. Each set of tests in the suite has a *.feature file and an associated *.py file. The feature files are in the tests/features directory. The Python files are in the tests/step_defs directory.

The tests/step_defs directory also includes various utility files that attempt to create reusable code objects that multiple test cases could use.

## What is missing from this MVP?

Coverage, coverage, and more coverage! The included tests are just the beginning of test coverage for this API. There are a multitude of use cases for /v1/audio/ that are not covered. There are also plenty of negative (i.e. failure) cases that need to ba addressed. I believe the project as it exists is a reasonable MVP and Proof of Concept.

## What could be improved?

The sentences which I used in the Feature files could (and perhaps should) be better worded so that the intent and operation of the test cases is more clear to non-technical interested parties.

The code is concentrated in the tests/step_defs directory. Work could be done to move code that is not a Step Definition out of that directory and into a better location. All the code was concentrated in this directory to simplify importing the code between Python files.

## Future Work (i.e. Future Sprint Tickets)

If I were to continue working on this project I would propose some improvements.

1. Reporting - I considered implementing the Allure Report (https://allurereport.org/) tool since it integrates with Pytest. But, since the tool has a Java requirement I decided against it for this assignment. I didn't want to introduce another language dependency at this time.
2. CI/CD - I didn't give much thought to integrating the framework into a CI/CD pipeline. It was not a requirement at this time, but it is something that should be addressed in a future sprint.
3. Integrating with a Dashboard visualization or BI tool - This is along the same lines as the Reporting item. Having the test run results appear in an Online Dashboard or having the results output to a BI tool could be useful for Project Managers, Program Managers, and Product Owners.

There is plenty of other work that could follow on to this project.