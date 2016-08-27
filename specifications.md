# Specifications

## Summary

This paper is about `happy-plumbers`, an idea for a data pipeline framework. Unlike, [`luigi`](http://luigi.readthedocs.io/en/stable/) or [`airflow`](https://github.com/apache/incubator-airflow), `happy-plumbers` is not concerned about data processing or job scheduling. It's a project managment tool: it supervises the development of a pipeline over time. 

## Introduction

Typical use-cases are the [EU Structural Funds](https://github.com/os-data/eu-structural-funds) or the [EU Farm Subsidies](https://github.com/os-data/farm-subsidies) projects. These projects are long-term collobarative endeavours carried out by people with a variety of skills. They have several stakeholders and a due-date. As for the data pipelines, they merge data from multiple countries and years and can be broken down into at least 4 steps:

- Source
- Extract
- Transform
- Load

Sourcing is a manual process, while ETL processes can be both manual or automatic. The point here is that `happy-plumbers` does not care about how you wrangle with the data. It just wants to know what's been done and what's left to do. Enter [Frictionless Data](http://frictionlessdata.io/).  We can use *data-packages* as milestones:

- Source -> `package.in.json` 
- Extract -> `data.in.csv`
- Transform -> `package.out.json` + `data.out.csv`
- Load

and *validate* the schema and data:

- Sourcing -> validate `package.in.json`
- Extract -> validate `data.in.csv`
- Transform -> validate `package.out.json` + validate `data.out.csv`
- Load

Typically, the 4 steps above would have to be run for each source of data. So for the above projects, that would mean each country and year. In the end, the state of the project at time `t` could be represented by a four-dimensional matrix `schema` x `data` x `country` x `year`, where each cell has 5 possible values: `missing`, `sourced` and `extracted`, `transformed` and `loaded`.

In a nutshell, that's all that `happy-plumbers` is. So if the pipeline and the data are stored on a local file system, it's a simple python script that validates the packages it finds and produces a report. I suggest that this be the proof-of-concept. Next, I would like to leverage the power of GitHub and turn `happy-plumbers` into a tool like `travis`. 

## Architecture

