from airflow.sdk import dag, task

@dag
def my_dag():
    
    @task
    def trainig_model(accuracy: int):
        return accuracy
    
    @task.branch
    def choose_training_model(accuracies: list[int]):
        if max(accuracies) > 2:
            return "accurate"
        return "inaccurate"
    
    @task.bash
    def accurate():
        return "echo 'accurate'"
    
    @task.bash
    def inaccurate():
        return "echo 'inaccurate'"
    
    accuracies = trainig_model.expand(accuracy=[1, 2, 3])
    best_model = choose_training_model(accuracies)
    accuracy = [accurate(), inaccurate()]

    accuracies >> best_model >> accuracy



my_dag()