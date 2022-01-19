import json
import os
import io
from time import time

class database_todolist():
    def __init__(self):
        self.database_file = "database_todo1.json"

        if os.path.isfile(self.database_file) and os.access(self.database_file, os.R_OK):
            print("JSON Database Loaded!")
            self.database = json.load(open(self.database_file))
        else:
            print ("Either file is missing or is not readable, creating file...")
            with io.open(os.path.join(self.database_file), 'w') as db_file:
                db_file.write(json.dumps({"todoData":[]}, indent=4))
                self.database = json.load(open(self.database_file))
        

    def folder(self,user_ID):
        folderName = []
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    folderName.append(j["folder"])
        return folderName

    def add_folder(self,user_ID,folderName):
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"].lower() == folderName.lower():
                        return "error"
                i["todolist"].append(
                                        {
                                            "folder": str(folderName),
                                            "taskfol_done": 0,
                                            "taskfol_undone": 0,
                                            "task" : []
                                        }
                                    )
                self.save_json()
                return "Add Folder : " + str(folderName)
        return "Error! >>> Add Folder : " + str(folderName)
    
    def add_folder2(self,user_ID,folderName):
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                i["todolist"].append(
                                        {
                                            "folder": str(folderName),
                                            "taskfol_done": 0,
                                            "taskfol_undone": 0,
                                            "task" : []
                                        }
                                    )
                self.save_json()
                return "Add Folder : " + str(folderName)
        return "Error! >>> Add Folder : " + str(folderName)

    def del_folder(self,user_ID,folderName):
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for count,j in enumerate(i["todolist"]):
                    if(j["folder"] == folderName):
                        i["taskall_done"] -= j["taskfol_done"]
                        i["taskall_undone"] -= j["taskfol_undone"]
                        i["todolist"].pop(count)
                        self.save_json()
                        return "Del Folder : " + str(folderName)
        return "Error! >>> Del Folder : " + str(folderName)

    def task(self,user_ID,in_folderName):
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"] == in_folderName:
                        return(j["task"])

    def add_task(self,user_ID,in_folderName,in_date,in_time,in_task):
        have_date = 0
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"] == in_folderName:
                        #print(j["task"])
                        i["taskall_undone"] += 1
                        j["taskfol_undone"] += 1
                        for k in j["task"]:
                            if k["date"] == in_date:
                                break
                            have_date +=1
                        if have_date == len(j["task"]):
                            ##print("no task in date")
                            
                            j["task"].append(
                                                {
                                                    "date": in_date,
                                                    "task_done" : 0,
                                                    "task_undone": 1,
                                                    "todo": [
                                                                {
                                                                    "time": in_time,
                                                                    "data": in_task,
                                                                    "done": False
                                                                }
                                                            ]
                                                }
                                            )
                            self.save_json()
                            return "Add Task : " + str(in_task) + " to Folder : " + str(in_folderName) + " in User : " + str(user_ID)
                        else:
                            #print("Added task in date")
                            k["task_undone"] += 1
                            have_time = 0
                            time_write = in_time.split(":")
                            time_read = []
                            for l in j["task"][have_date]["todo"]:
                                time_read.append(l["time"].split(":"))

                            for m in time_read:
                                print(m)
                                if int(time_write[0]) > int(m[0]):
                                    have_time += 1
                                elif int(time_write[0]) < int(m[0]):
                                    break
                                elif int(time_write[0]) == int(m[0]):
                                    #print(time_write[1],m[1])
                                    if int(time_write[1]) > int(m[1]) :
                                        have_time += 1
                                    elif int(time_write[1]) < int(m[1]) :
                                        break
                                    elif int(time_write[1]) == int(m[1]):
                                        have_time += 1
                                        break
                                
                            j["task"][have_date]["todo"].insert(have_time,{"time": in_time,"data": in_task,"done": False})
                            self.save_json()
                            return "Add Task : " + str(in_task) + " to Folder : " + str(in_folderName) + " in User : " + str(user_ID)

    def del_task(self,user_ID,in_folderName,in_date,in_time,in_task):
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"] == in_folderName:
                        for count_task,k in enumerate(j["task"]):
                            if k["date"] == in_date:
                                for count_todo,l in enumerate(k["todo"]):
                                    if l["time"] == in_time and l["data"] == in_task:
                                        if l["done"] == True:
                                            k["task_done"] -= 1
                                            j["taskfol_done"] -= 1
                                            i["taskall_done"] -= 1
                                        else:
                                            k["task_undone"] -= 1
                                            j["taskfol_undone"] -= 1
                                            i["taskall_undone"] -= 1
                                        k["todo"].pop(count_todo)
                                        if(len(k["todo"]) == 0):
                                            j["task"].pop(count_task)
                                        self.save_json()
                                        return 0
    
    def done_task(self,user_ID,in_folderName,in_date,in_time,in_task):
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"] == in_folderName:
                        for k in j["task"]:
                            if k["date"] == in_date:
                                for l in k["todo"]:
                                    if l["time"] == in_time and l["data"] == in_task and l["done"] == False:
                                        l["done"] = True

                                        k["task_undone"] -= 1
                                        k["task_done"] += 1

                                        j["taskfol_undone"] -= 1
                                        j["taskfol_done"] += 1

                                        i["taskall_undone"] -= 1
                                        i["taskall_done"] += 1

                                        self.save_json()
                                        return 0

    def undone_task(self,user_ID,in_folderName,in_date,in_time,in_task):
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"] == in_folderName:
                        for k in j["task"]:
                            if k["date"] == in_date:
                                for l in k["todo"]:
                                    if l["time"] == in_time and l["data"] == in_task and l["done"] == True:
                                        l["done"] = False

                                        k["task_undone"] += 1
                                        k["task_done"] -= 1

                                        j["taskfol_undone"] += 1
                                        j["taskfol_done"] -= 1

                                        i["taskall_undone"] += 1
                                        i["taskall_done"] -= 1

                                        self.save_json()
                                        return 0
    
    def display_undone_task(self,user_ID,in_folderName):
        display = []
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"] == in_folderName:
                        for k in j["task"]:
                            if k["task_undone"] != 0:
                                display.append("======= Date : "+ k["date"]+" =======")
                                display.append("Done : " + str(k["task_done"]) + "     Undone : " + str(k["task_undone"]))
                                display.append("            ")
                                for l in k["todo"]:
                                    if l["done"] == False:
                                        display.append(l["time"]+" - "+l["data"])
                                display.append("")
        return display
    
    def display_done_task(self,user_ID,in_folderName):
        display = []
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"] == in_folderName:
                        for k in j["task"]:
                            if k["task_done"] != 0:
                                display.append("======= Date : "+ k["date"]+" =======")
                                display.append("            ")
                                for l in k["todo"]:
                                    if l["done"] == True:
                                        display.append(l["time"]+" - "+l["data"])
                                display.append("")
        return display
    
    def display_all_stat(self,user_ID):
        display = []
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                display.append(i["taskall_done"]+i["taskall_undone"])
                display.append(i["taskall_done"])
                display.append(i["taskall_undone"])
        return display
    
    def display_fol_stat(self,user_ID,in_folderName):
        display = []
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"] == in_folderName:
                        display.append(j["taskfol_done"]+j["taskfol_undone"])
                        display.append(j["taskfol_done"])
                        display.append(j["taskfol_undone"])
        return display

    def save_json(self):
        print("JSON Database Save!")
        with open(self.database_file, 'w', encoding='utf-8') as f:
            json.dump(self.database, f, ensure_ascii=False, indent=4)
            
    def testsave_json(self):
        print("JSON Test Database Save!")
        with open('database_test.json', 'w', encoding='utf-8') as f:
            json.dump(self.database, f, ensure_ascii=False, indent=4)
    
    def loginCheck(self,in_username,in_password):
        for i in self.database["todoData"]:
            if i["username"] == in_username.lower():
                if i["password"] == in_password:
                    return i["user_id"]
                else:
                    return "error"
        return "error"
    
    def register_user(self,input_username,input_password):
        user_id = 0
        for i in self.database["todoData"]:
            user_id +=1
            if i["username"] == input_username.lower():
                return False
        self.database["todoData"].append(
                                            {
                                                "user_id": user_id,
                                                "username": input_username.lower(),
                                                "password": input_password,
                                                "taskall_done": 0,
                                                "taskall_undone": 0,
                                                "todolist": []
                                            }
                                        )
        print("Add User : " + str(input_username.lower()) + " Password : " + str(input_password) + " user_id : " + str(user_id))
        self.save_json()
        return True

    def statFol(self,user_ID):
        labels_fol = []
        alltask_fol = []
        donetask_fol = []
        undonetask_fol = []
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    labels_fol.append(j["folder"])
                    alltask_fol.append(j["taskfol_done"]+j["taskfol_undone"])
                    donetask_fol.append(j["taskfol_done"])
                    undonetask_fol.append(j["taskfol_undone"])
        return [labels_fol,alltask_fol,donetask_fol,undonetask_fol]
    
    def statTodo(self,user_ID,in_folder):
        labels_date = []
        alltask_todo = []
        donetask_todo = []
        undonetask_todo = []
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"] == in_folder:
                        for k in j["task"]:
                            labels_date.append(k["date"])
                            alltask_todo.append(k["task_done"]+k["task_undone"])
                            donetask_todo.append(k["task_done"])
                            undonetask_todo.append(k["task_undone"])
        return [labels_date,alltask_todo,donetask_todo,undonetask_todo]
    
    def import_data(self,user_ID,in_filepath):
        load_data = json.load(open(in_filepath))
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                i["taskall_done"] = load_data["data_in"]["taskall_done"]
                i["taskall_undone"] = load_data["data_in"]["taskall_undone"]
                i["todolist"] = load_data["data_in"]["todolist"]
                self.save_json()
                return True
            
    def export_data(self,user_ID,in_filepath):
        data_out = {}
        data_col = {}
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                
                data_col["taskall_done"] = i["taskall_done"]
                data_col["taskall_undone"] =i["taskall_undone"]
                data_col["todolist"] = i["todolist"]
                data_out["data_in"] = data_col
                with open(in_filepath+"/"+i["username"]+".json", 'w') as f:
                    json.dump(data_out, f, indent=4)
                return True


if __name__ == '__main__':
    data = database_todolist()
    #print(data.database)
    #print(data.folder(0))
    #print(data.task(0,"School"))
    """
    print(data.add_task(0,"School","11/1/22","09:10","goto Chonlada"))
    print("================================")
    print(data.task(0,"School"))
    print("================================")
    print(data.del_task(0,"School","11/1/22","09:10","goto Chonlada"))
    print("================================")
    print(data.task(0,"School"))
    print("================================")
    """
    #print(data.display_task(0,"School"))
    #print(data.add_folder(0,"BOMB"))
    #print(data.folder(0))
    #print(data.del_folder(0,"BOMB"))
    #print(data.folder(0))
    #print(data.task(0,"BOMB"))
    #print(data.del_task("Work",0))
    #print(data.add_folder("BOMB"))
    #print(data.database)
    #print("====================================")
    #print(data.del_folder("BOMB"))
    #print(data.database)
    #print("====================================")
    #print(data.save_json())
    #print(data.register_user("Netipat","1234"))
    #print(data.testsave_json())
    #print(data.register_user("Netipat","1234"))
    #print(data.statFol(0))
    
    #data.import_data(0,"D:\Github\TODO-List-App\dataimport.json")
    data.export_data(0,"D:\Github\TODO-List-App\dataimport.json")
    
    #print(data.database)