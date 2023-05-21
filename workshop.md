## Project presentation and setup

- Model graph
  [ ] TODO: print graph viz
- project organization
- basic tools
  - jupyter
  - pytest
  - django_extensions
- data generation

  - faker
  - binomial distrib

- postgres conf
  - Memory usage
  - disk space

## 1st example list_readers_per_book

- naive implementation
- show how to measure perf

## 2nd example: indexes and order by

- list reviews endpoint
  - filter on rating, date (library id)
  - order by id, date, rating

## 3rd example: annotations

- ArrayAgg
- Subqueries
- Python join
- CTE (django cte)

## WRITE queries

- generate data script
  - use bulks
- updates
  - use iterators for memory
    https://nextlinklabs.com/resources/insights/django-big-data-iteration

## TODO

- `django_cte`
- `assert_django_queries`
