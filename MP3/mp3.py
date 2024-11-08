#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Eric Lazarski
# 2/22/2019
# CPSC 57100 - Artificial Intelligence 1
# Spring 2019
# MP3

import constraint as c
import numpy as np
import pandas as pd

# to make output pretty later
replacements = dict()
replacements[-np.inf] = "Not Taken"
y = 0
for i in range(0, 14):
    term = "Year {0} {1} {2}"
    if i % 6 == 0:
        y += 1
    
    season = i % 6
    if season == 0 or season == 1:
        season = "Fall"
    elif season == 2 or season == 3:
        season = "Spring"
    else:
        season = "Summer"
    
    t = i % 2
    
    replacements[i] = term.format(y, season, t + 1)

# load data - pd.read_excel did not work right on Linux
courses = pd.read_excel('csp_course_rotations.xlsx', sheet_name='course_rotations')
prereqs = pd.read_excel('csp_course_rotations.xlsx', sheet_name='prereqs')
#prereqs = pd.read_csv('prereqs.csv')

# generate CSP
problem = c.Problem()
for index, row in courses.iterrows():
    # domain of course is only when it is offered
    times = range(0, 6)
    courseOffered = row.as_matrix()[2:]
    domain = []
    for y in range(0,3): # 3 years
        for i in times:
            # if the course is offered and we aren't past y3f2
            if courseOffered[i] == 1 and not (y == 2 and i > 1):
                domain.append(i + 6*y)
    
    # if foundation course, it MUST be taken
    if row.Type == "elective":
        domain.append(c.Unassigned)

    # add course to problem
    problem.addVariable(row.Course, domain)

# generate constraints
# student may only take one course at a time
problem.addConstraint(c.AllDifferentConstraint())

# prerequisites must be followed
for index, row in prereqs.iterrows():
    row = row.as_matrix()
    problem.addConstraint(c.FunctionConstraint(lambda c1, c2: c1 < c2), list(row))

# student must start in Y1F1 finish Y3F2
problem.addConstraint(c.SomeInSetConstraint(set=[0, 13], n=2, exact=True))

# student must take 3 out of the 8 elective courses
electives = []
for index,row in courses.iterrows():
    if row.Type == "elective":
        electives.append(row.Course)
        #problem.addConstraint(c.SomeNotInSetConstraint([c.Unassigned]), [row.Course])
        
problem.addConstraint(c.SomeNotInSetConstraint(set=[c.Unassigned], n=3), electives)

# solve CSP
solutions = problem.getSolutions()

# print data
print("CLASS: Artificial Intelligence, Lewis University")
print("NAME: Eric Lazarski")
print("")

print("START TERM = {0}".format(replacements[0]))
print("Number of Possible Degree Plans is {0}".format(len(solutions)))
print("")

print("Sample Degree Plan")
# make output pretty
s = pd.Series(solutions[0])
s.replace(to_replace=c.Unassigned, value=-np.inf, inplace=True)
s.sort_values(inplace=True)
s.replace(replacements, inplace=True)
print(s.to_string())