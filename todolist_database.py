import json
from time import time

class database_todolist():
    def __init__(self):
        print("JSON Database Loaded!")
        self.database = json.load(open('database_todo.json'))
        #self.user_database = json.load(open('database_user.json'))

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
                #print(i["todolist"])
                i["todolist"].append(
                                        {
                                            "folder": str(folderName),
                                            "task_done": 0,
                                            "task_undone": 0,
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
                        for k in j["task"]:
                            if k["date"] == in_date:
                                break
                            have_date +=1
                        if have_date == len(j["task"]):
                            ##print("no task in date")
                            j["task"].append({"date": in_date, "task_done" : 0, "task_undone": 1, "todo":[{"time": in_time,"data": in_task,"done": False}]})
                            self.save_json()
                            return "Add Task : " + str(in_task) + " to Folder : " + str(in_folderName) + " in User : " + str(user_ID)
                        else:
                            #print("Added task in date")
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
                        for k in j["task"]:
                            if k["date"] == in_date:
                                for count,l in enumerate(k["todo"]):
                                    if l["time"] == in_time and l["data"] == in_task:
                                        k["todo"].pop(count)
                                        self.save_json()

    def display_task(self,user_ID,in_folderName):
        display = []
        for i in self.database["todoData"]:
            if i["user_id"] == user_ID:
                for j in i["todolist"]:
                    if j["folder"] == in_folderName:
                        for k in j["task"]:
                            display.append("====== Date : "+ k["date"]+" ======")
                            display.append("")
                            for l in k["todo"]:
                                display.append(l["time"]+" - "+l["data"])
                            display.append("")
        return display

    def save_json(self):
        print("JSON Database Save!")
        with open('database_todo.json', 'w', encoding='utf-8') as f:
            json.dump(self.database, f, ensure_ascii=False, indent=4)

    def username(self) :
        user = [] 
        for i in self.database["todoData"] :
            user.append(i["username"])
        return user

    def password(self) :
        password = [] 
        for i in self.database["todoData"] :
            password.append(i["password"])
        return password



if __name__ == '__main__':
    data = database_todolist()
    #print(data.database)
    #print(data.folder(0))
    #print(data.task(0,"School"))
    print(data.add_task(0,"School","11/1/22","09:10","goto Chonlada"))
    print("================================")
    print(data.task(0,"School"))
    print("================================")
    print(data.del_task(0,"School","11/1/22","09:10","goto Chonlada"))
    print("================================")
    print(data.task(0,"School"))
    print("================================")
    print(data.display_task(0,"School"))
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