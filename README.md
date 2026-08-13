# Supermarket Product Placement Optimisation

> Probabilistic simulation of customer purchasing behaviour and supermarket layout optimisation.

## Overview

This project investigates how the spatial organisation of products in a supermarket can influence customer purchasing behaviour and the resulting revenue.

The project was developed as part of a French scientific research project (TIPE).

The approach combines probabilistic modelling, stochastic simulation, pathfinding and spatial optimisation. A simplified supermarket is represented a 4 × 4 grid, where customer behaviour and movement are simulated under predefined probabilistic assumptions (purchasing probabilities and product relationships).

Different spatial configurations are then compared according to the average revenue generated per simulated customer.

## Objective

The objective is to determine whether the spatial configuration of supermarket departments can influence simulated customer behaviour and to identify a configuration that maximise expected revenue.

Three types of configurations are studied:

- random configuration
- proximity-based configuration
- distance-based configuration

The problem can therefore be formulated as a comparison between different configurations according to a defined performance metric:

$$
\text{Expected revenue per customer}
$$

## Data and assumptions

No real customer transaction data were used in this project, as such data are confidential and were not publicly available.

Instead, the model was constructed using publicly available information and manually defined assumptions designed to represent plausible purchasing behaviour.

Three main datasets are used:

### Initial shopping-list probabilities

Each product is assigned a probability representing the likelihood that it is included in a customer's initial shopping list.

These probabilities are used to generate different simulated customer scenarios (represented by their shopping list).

### Product relationship matrix

A matrix assigns a numerical value to each pair of products, representing the assumed strength of their purchasing relationship.

These relationships are used to model how encountering products during a customer's path through the supermarket can influence additional purchases.

### Product prices

Each product is assigned an average price.

These values are used to calculate the total value of each simulated customer's purchases and evaluate the performance of each spatial configuration.

The datasets and relationships used in the simulation are model assumptions rather than empirical measurements. The results should therefore be interpreted within the limits of the model.

## Methodology

### 1. Environment Modelling

The supermarket is represented as a 4 × 4 discrete grid.

Each cell corresponds to a department, with the entrance and checkout represented by specific locations.

The model contains:
- 15 departments;
- 44 products;
- a discrete 2D environment;
- constrained horizontal and vertical movement.

This representation provides a simplified environment in which spatial configurations can be generated and compared.

### 2. Generating Customer Scenarios

For each simulated customer, an initial shopping list is generated probabilistically.

Each product has an associated probability of being included in the list.

A random draw is performed for each product, producing different customer scenarios while preserving the assumed purchasing frequencies.

This stochastic approach allows each spatial configuration to be evaluated across multiple simulated customers, each with different purchasing behaviour.

### 3. Computing Purchase Probabilities

The product relationship matrix provides the assumed purchasing relationships between products.

For each simulated customer, the initial shopping list is used to compute a purchase probability for each product that is not already on the list. This probability is based on the relationships between the products already selected and the remaining products.

These probabilities are then used during the customer's journey through the supermarket to simulate additional purchases.

If a product is encountered but is not purchased, its purchase probability is reduced by half for subsequent encounters. This models a decreasing likelihood of purchasing a product after repeatedly encountering it without buying it. 

### 4. Customer Pathfinding

Customers move through the supermarket using horizontal and vertical movements only.

The model assumes that a customer travelling towards a target department will follow a shortest available path. A Breadth-First Search (BFS) algorithm is therefore used to determine this path.

This is a simplified representation of human behaviour rather than a realistic pedestrian model. Its purpose is to introduce a spatial component into the simulation: departments encountered along the path can influence the customer's purchasing decisions. They are considered as potential opportunities for additional purchases.

### 5. Spatial Configuration Strategies

Three different configuration strategies are compared, two of them use department relationships to place them.

Department relationships are derived from the product relationship matrix by aggregating the relationships between products belonging to each department. A strong relationship between two departments therefore indicates that their products have strong assumed purchasing relationships.

#### Random configuration

Departments are randomly distributed across the available grid positions.

#### Proximity-based layout

Departments with stronger purchasing relationships are preferentially placed close to one another.

#### Distance-based layout

Departments with stronger purchasing relationships are preferentially placed further apart.

### 6. Revenue evaluation

For each simulated customer, the total value of the purchased products is calculated using the assigned average product prices.

Each configuration is evaluated over multiple simulated customers.

The average spending per customer is then used as the main performance metric.

The objective is therefore to maximise the revenue per customer.

## Results

The simulation produced a counter-intuitive result: in the current model, the random configuration generally generated higher revenue than the two probability-based configurations.

This result suggests that the assumptions used in the model have a significant influence on the outcome.

Several limitations were identified:
- the assumptions used to construct the purchasing probabilities
- the simplified representation of customer behaviour;
- the absence of empirical transaction data.

These limitations provide potential directions for improving the model.

## Technologies

- Python
- pandas
- NumPy
- matplotlib
- random

## Repository Structure

```text
.
├── code/
├── data/
├── figures/
├── presentation/
└── README.md
