# Code Repository for Crafting an Error Handling Strategy (Python)

This repository provides code used for exercises and demonstrations
included in the Python version of the [Crafting an Error Handling Strategy](https://learn.temporal.io/courses/crafting-error-strategy)
training course.

It's important to remember that the example code used in this course was designed 
to support learning a specific aspect of Temporal, not to serve as a ready-to-use 
template for implementing a production system.

For the exercises, make sure to run `temporal server start-dev --ui-port 8080 --db-filename clusterdata.db` 
in one terminal to start the Temporal server. For more details on this command,
please refer to the `Setting up a Local Development Environment` chapter in the
course. 

*Note: If you're using the Gitpod environment to run this exercise, you can skip this step.*

## Hands-On Exercises

| Directory Name                           | Exercise                                                    |
| :--------------------------------------- | :---------------------------------------------------------- |
| `exercises/handling-errors`              | [Exercise 1](exercises/handling-errors/README.md)           |
| `exercises/non-retryable-error-types`    | [Exercise 2](exercises/non-retryable-error-types/README.md) |
| `exercises/saga-pattern`        | [Exercise 3](exercises/saga-pattern/README.md)                       |

## Instructor-Led Demonstrations

| Directory Name            | Description                                                         |
| :------------------------ | :------------------------------------------------------------------ |
| `demos/error-propagation` | [Cross-Language Error Propagation](demos/error-propagation/README.md) |

## Reference

The following links provide additional information that you may find helpful as
you work through this course.

- [General Temporal Documentation](https://docs.temporal.io/)
- [Temporal Python SDK Documentation](https://python.temporal.io/)
- [Python Language Documentation](https://docs.python.org/3/)
- [Python Packaging and Virtual Environment Documentation](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments)
- [GitPod Documentation: Troubleshooting](https://www.gitpod.io/docs/troubleshooting)

## Exercise Environment for this Course

You can launch an exercise environment for this course in GitPod by clicking the
button below:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/temporalio/edu-errors-python-code)

Alternatively, you can perform these exercises directly on your computer. Refer 
to the instructions about setting up a local development environment, which you'll 
find in the "About this Course" chapter.
