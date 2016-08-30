## Overview

### Abstract

This paper is about `plumbers`, an idea for a data pipeline framework. Contrary to [`luigi`](http://luigi.readthedocs.io/en/stable/) or [`airflow`](https://github.com/apache/incubator-airflow), `plumbers` is not concerned about data processing or job scheduling. It's a project managment tool: it supervises the development of a pipeline over time. 

### Summary

Typical use-cases are the [EU Structural Funds](https://github.com/os-data/eu-structural-funds) or the [EU Farm Subsidies](https://github.com/os-data/farm-subsidies) projects. These projects are long-term collaborative endeavours carried out by people with a variety of skills. They have several stakeholders and a due-date. As for the data pipelines, they merge data from multiple countries and years and can be broken down into at least 4 steps:

- Source
- Extract
- Transform
- Load

Sourcing is a manual process, while ETL processes can be both manual or automatic. The point here is that `plumbers` does not care about how you wrangle with the data. It just wants to know what's been done and what's left to do. Enter [Frictionless Data](http://frictionlessdata.io/).  We can use *data-packages* as milestones:

- Source -> `package.in.json` 
- Extract -> `data.in.csv`
- Transform -> `package.out.json` + `data.out.csv`
- Load

and *validate* the schemas and data files:

- Sourcing -> validate `package.in.json`
- Extract -> validate `data.in.csv`
- Transform -> validate `package.out.json` + validate `data.out.csv`
- Load

Typically, the 4 steps would have to be run for each *pipe*. So for the above projects, that would mean each country and year. In the end, the state of the project could be represented (simply-put) by a matrix `country` x `year`, where each cell has 5 possible values: `wanted`, `sourced` and `extracted`, `transformed` and `loaded`.

### Proof-of-concept

In a nutshell, that's all that `plumbers` is. So if the pipeline and the data are stored on a local file system, it's a simple python script that validates the packages it finds and produces a report. I suggest that this be the proof-of-concept. Next, I would like to leverage the power of GitHub and turn `plumbers` into a tool like `travis`. 

## Specifications

### Configuration

The application is driven from a bunch of `data-package` and `goodtables` validators inside the `validation` directory.

```
validation/
    eu_cohesion_funds.sourced.schema.json
    eu_cohesion_funds.extracted.data.json
    eu_cohesion_funds.transformed.schema.json
    eu_cohesion_funds.transformed.data.json
```

Validation settings are set globally: all pipes have the same milestones. The output of the validation,  `report.yaml`, should look something like :

```
execution:
  started: 12:23:45 UTC
  finished: 13:24:46 UTC

validation:
  FN.2007-2014.sourced.schema.json: valid
  FN.2014-2022.sourced.schema.json: valid
  FN.2007-2014.extracted.data.csv: valid
  FN.2014-2022.extracted.data.1.csv: valid
  FN.2014-2022.extracted.data.2.csv: valid
  FN.2007-2014.transformed.schema.json: valid
  FN.2014-2022.transformed.schema.json: valid
  FN.2007-2014.transformed.data.csv: valid
  FN.2014-2022.transformed.data.1.csv: valid
  FN.2014-2022.transformed.data.2.csv: invalid

errors:
  FN.2014-2022.transformed.data.2.csv: 
    - error message number 1
    - error message number 2
```
