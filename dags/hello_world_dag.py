from airflow.sdk import dag, task

@dag
def hello_world_dag():
    @task
    def first_task():
        print("-" * 5, end="")
        print(" WORKFLOW STARTED ", end="")
        print("-" * 5)

    @task
    def hello_world():
        print("Hello, World!")

    @task
    def final_task():
        print("-" * 5, end="")
        print(" WORKFLOW COMPLETED ", end="")
        print("-" * 5)

    first_task() >> hello_world() >> final_task()


hello_world_dag = hello_world_dag()
