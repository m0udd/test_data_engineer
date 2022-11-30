# Data Engineering Test

## Description
Build a resilient data pipeline and find the relation between drugs and their mentions in scientific articles.
Generate a JSON graph as the result. 

## Architecture
Here is an implementation of Extract / Load / Transform (ELT) data pipeline with three distinct data zone.

1) The RAW zone is used to store the raw data without any modifications.
2) The MINING zone is used to store the clean/merged data.
3) The GOLD zone is used to sore the meaningful data for business/corporate usage.

In input we have:
* **[clinical_trials.csv](plugins/data/test/clinical_trials.csv)**
* **[drugs.csv](plugins/data/test/drugs.csv)**
* **[pubmed.csv](plugins/data/test/pubmed.csv)**
* **[pubmed.json](plugins/data/test/pubmed.json)**

In output we have:
* **[published_drugs.json](plugins/data/gold/published_drugs.json)**

## How to run ~~the world~~ the code?
We have two options to run this code:

### Dev mode

```Shell
cd test_data_engineer/plugins 
python3 run_full_data_pipeline.py 
```

### Production mode (DAG with Airflow)
```Shell
docker-compose up 
```
Then you can go to http://localhost:8080 and run the dag called 'test_de_dag'
* Login: airflow
* Pass: airflow


* /!\ This Docker file is not production ready...
 
### Ad-Hoc 
```Shell
cd test_data_engineer/plugins 
python3 ad_hoc.py 
```

## SQL
All sql requests is here : 
**[SQL Scipt](sql/request.py)**
```Shell
cd test_data_engineer/sql 
python3 request.py 
```

## Pour aller plus loin

 ***Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses
volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?***

* Utiliser un framework de calcul distribué (ex. Apache Spark) avec un cluster adapté. 

*J'ai déjà travailler avec PySpark sur une volumétrie +8 milliards de lignes, aucun problème avec un bon dimensionnement et des serveurs type 'high-mem'.*

* Utiliser un service cloud managé (ex. Google BigQuery/DataFlow...).

* Utiliser une seule machine avec un mécanisme de lecture par batch + calcul parallèle (ex. Pandas/Dask).

***Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de
telles volumétries ?***

* Faire une étude des coûts.
* Etudier la possibilité de faire du traitement 'streaming'.
* Mettre en place de la gouvernance des données.
* Utiliser un pipeline CI/CD.
* Bien orchestrer les jobs (Airflow par ex.).
* Ajouter les tests unitaires.
* Finaliser le logging.
* Bien comprendre les enjeux métiers et mettre en place un data cleaning efficace.