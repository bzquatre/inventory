from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime
import platform,json
class LoginScreen(Screen):
    def toggle_password_visibility(self, *args):
        password_input = self.ids.password_input
        password_input.password = not password_input.password
        password_input.icon_right = "eye" if password_input.password else "eye-off"


class MainScreen(Screen):
    pass

class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    
    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

# After creating the database.py
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk


    def delete_item(self, the_list_item):
        '''Delete the task'''
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)
        # Here
class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''
class MainApp(MDApp):
    task_list_dialog = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.user_data_dir)
        if platform.system() == 'Android':
            # Create a JsonStore in the app's internal storage directory
            store = JsonStore('internal://data.json')
        else:
            self.store = JsonStore(self.user_data_dir + '/data.json')
    
    def build(self):
        
        if self.store._data!={}:
            try:
                refreshToken=self.store.get('user')["refresh"]
                self.user = self.refresh_login(refreshToken)
            except  Exception as e:
                print(e)
            else:
                self.root.current='main'

        return super().build()
       
    def refresh_login(self,refresh):
        data={
            "refresh": refresh
        }
        headers = {"Content-Type": "application/json"} 
        api_url = "https://dc.opu.dz/api/token/refresh/"
        UrlRequest(api_url,method="POST",req_body=json.dumps(data), req_headers=headers,
                   on_success=self.on_success, on_failure=self.on_failure, on_error=self.on_error)
    def login(self,username,password):
        self.username=username
        data={"username":username,"password": password}
        headers = {"Content-Type": "application/json"} 
        api_url = "https://dc.opu.dz/api/token/"
        UrlRequest(api_url,method="POST",req_body=json.dumps(data), req_headers=headers,
                   on_success=self.on_success, on_failure=self.on_failure, on_error=self.on_error)
    def logout(self):
        return
        self.store.clear()

    def on_success(self, request, result):
        # Handle the successful API response
        try:
            self.store.put('user', username=self.username, refresh=result["refresh"],access=result['access'])
        except:
            self.store['user']["access"]=result['access']
        self.root.transition.direction = 'left'
        self.root.current = 'main'

    def on_failure(self, request, result):
        # Handle the failure (non-HTTP error status)
        #self.root.ids.label_api.text = 'Request failed'
        pass

    def on_error(self, request, result):
        # Handle the error (network error, etc.)
        #self.root.ids.label_api.text = 'Request error'
        pass

    # Showing the task dialog to add tasks
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Ajouter un Article",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def on_start(self):
        # Load the saved tasks and add them to the MDList widget when the application starts
        """
        try:
            completed_tasks, incompleted_tasks = db.get_tasks()

            if incompleted_tasks != []:
                for task in incompleted_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0],text=task[1], secondary_text=task[2])
                    self.root.ids.container.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0],text='[s]'+task[1]+'[/s]', secondary_text=task[2])
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        except Exception as e:
            print(e)
            pass
        """
        pass
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        '''Add task to the list of tasks'''
        # print(task.text, task_date)
        created_task = db.create_task(task.text, task_date)

        # return the created task details and create a list item
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk=created_task[0], text='[b]'+created_task[1]+'[/b]', secondary_text=created_task[2]))
        task.text = ''

if __name__ == '__main__':
    MainApp().run()