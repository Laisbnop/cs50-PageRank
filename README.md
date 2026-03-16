# PageRank Algorithm

Implementation of Google's PageRank algorithm in Python.

## Description

This project implements the **PageRank algorithm**, originally developed by Google to rank web pages based on their importance.

The algorithm analyzes the links between pages and assigns a probability score representing how likely a user is to arrive at a particular page.

Pages with more important incoming links receive a higher rank.

## Concepts

- Graph algorithms
- Probability
- Markov chains
- Iterative algorithms

## Technologies

Python

## How It Works

The program analyzes a set of HTML pages and builds a graph of links between them.

Two approaches are used to compute PageRank:

### 1. Sampling

Simulates a random user clicking links and estimates page importance based on visit frequency.

### 2. Iteration

Repeatedly updates PageRank values until they converge.

## How to Run

Run the program with a corpus of HTML pages:
