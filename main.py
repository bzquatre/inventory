from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
import json
class LoginScreen(Screen):
    def toggle_password_visibility(self, *args):
        password_input = self.ids.password_input
        password_input.password = not password_input.password
        password_input.icon_right = "eye" if password_input.password else "eye-off"


class MainScreen(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        
        return 
        self.auth = Firebase.auth()
        try:
            refreshToken=json.load(open("user.json"))["refreshToken"]
            self.user = self.auth.refresh(refreshToken)
        except  Exception as e:
            print(e)
            
        else:
            self.root.current='main'
    
    def login(self,email,password):
        return
        self.auth=Firebase.auth()
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            with open("user.json", 'w') as json_file:
                json.dump(user, json_file, indent=4)
        except Exception as e:
            pass
        else:
            self.root.transition.direction = 'left'
            self.root.current = 'main'

    def logout(self):
        self.auth.current_user = None  # Clear the current user
        self.root.transition.direction = 'right'
        self.root.current = 'login'
        with open("user.json","w") as user:
            user.write('')

    

if __name__ == '__main__':
    MainApp().run()