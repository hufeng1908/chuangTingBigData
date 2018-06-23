hdfs dfs -rm -r /user/test/test_out
#/opt/cloudera/parcels/CDH/lib/spark/bin/
#/opt/cloudera/parcels/CDH/lib/spark/bin/
/opt/cloudera/parcels/CDH/lib/spark/bin/spark-submit  \
--master yarn \
--deploy-mode client \
--num-executors 8 \
--executor-memory 1G \
--archives hdfs:///user/tools/anaconda2.zip#anaconda2 \
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./anaconda2/anaconda2/bin/python \
test_sparksql_hive.py