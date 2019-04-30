# Where are the DUPs?

## Problem description
A Bug Tracking System is an integral part of a robust software development infrastructure, as it helps keep all requests concerning the software centralized (such as new features, improvements or identified issues). As the software grows, the work that is required to manage bug triage also increases. One of the challenges involved in the use of bug trackers is the bug report duplication problem. In Mozilla, for instance, more than 500 bug reports are marked as duplicates per month. This is important because the triager needs to spend time in analyzing the bug and identifying if it has been previously reported which ultimately increase the cost of Software Maintenance. In view of this need, our paper will focus on finding better and more efficient ways classify duplicate bugs. 

## Motivation
The intent of this empirical approach is mainly to learn more about information retrieval (IR) and classification algorithms. Moreover, we seek to determine how a classification algorithm can help improve the effort required to identify bug duplicates.

## Requirements
The project was developed using:
* PyCharm Professional 2018.3 
* Python 3.7

## Libraries used:
* Scikit-learn
* NumPy

## Installation
1. Modify the ``filtered_bug_reports.args`` property to indicate the bug reports XML file location. 
2. Run main.py
3. Review the console results

## Authors
* Virginia Pujols <vp2532@rit.edu> - MS Software Engineering Student at RIT 
* Cervantes Hernandez <crh2302@rit.edu> - MS Software Engineering Student at RIT 
