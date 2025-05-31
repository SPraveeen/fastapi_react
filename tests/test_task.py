

def test_create_task(client):
    task_data={
        "taskname":"first task",
        "description":"first description",
        "status":"first status"
    }
    res=client.post("/tasks/",json=task_data)
    assert res.status_code==201
    new_task=res.json()
    assert new_task['name']==task_data['taskname']
    assert new_task['description']==task_data['description']
    assert new_task['status']==task_data['status']

def test_get_all_tasks(client,test_tasks):
    res=client.get("/tasks/")
    assert res.status_code==200