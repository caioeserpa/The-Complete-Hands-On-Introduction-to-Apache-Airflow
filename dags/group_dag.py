from airflow import DAG
from airflow.operators.bash import BashOperator
#from airflow.operators.subdag import SubDagOperator
from datetime import datetime
#from subdags.subdag_downloads import subdag_downloads
#from subdags.subdag_transforms import subdag_transforms

from groups.group_downloads import download_tasks 
from groups.group_transforms import transform_tasks
 
with DAG('group_dag',
        start_date=datetime(2022, 10, 3), 
        schedule_interval='@daily',
        catchup=False) as dag:
 
    args = {'start_date': dag.start_date,
            'schedule_interval': dag.schedule_interval,
            'catchup':dag.catchup}
   
   
    downloads = download_tasks()
    
    # downloads=SubDagOperator(
    #     task_id='downloads',
    #     subdag=subdag_downloads(dag.dag_id,
    #                             'downloads',
    #                             args)
    # )
     
    
    
    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )
 
    transforms = transform_tasks()
    
    # transforms = SubDagOperator(
    # task_id='transforms',
    # subdag=subdag_transforms(dag.dag_id,
    #                          'transforms',
    #                          args)
    # )
 
    downloads >> check_files >> transforms
    
    
    