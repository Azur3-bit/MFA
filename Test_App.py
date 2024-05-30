from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

CORRECT_PASSWORD = "123"
CORRECT_UPI_PIN = "741"

class FingerPrint:
    def open(self):
        # Placeholder for actual fingerprint opening code
        pass

    def verify(self):
        # Placeholder for actual fingerprint verification code
        return True

    def close(self):
        # Placeholder for actual fingerprint closing code
        pass

class MyApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        
        heading_label = Label(text="SRM HACKATHON", font_size=24)
        self.root.add_widget(heading_label)
        
        self.username_input = TextInput(hint_text='Enter your username')
        self.root.add_widget(self.username_input)
        
        password_button = Button(text='Password', size_hint=(0.5, 0.5), on_release=self.authenticate_with_password)
        self.root.add_widget(password_button)
        
        biometric_button = Button(text='Biometric', size_hint=(0.5, 0.5), on_release=self.fingerprint_authentication)
        self.root.add_widget(biometric_button)
        
        return self.root

    def authenticate_with_password(self, instance):
        if self.username_input.text and self.username_input.text == CORRECT_PASSWORD:
            self.show_popup("Authentication", "Password authenticated successfully!")
            self.open_payment_gateway()
        else:
            self.show_popup("Error", "Incorrect password.")
    
    def fingerprint_authentication(self, instance):
        fingerprint = FingerPrint()
        fingerprint.open()
        if fingerprint.verify():
            self.show_popup("Authentication", "Fingerprint authenticated successfully!")
            self.open_payment_gateway()
        else:
            self.show_popup("Error", "Fingerprint authentication failed.")
        fingerprint.close()
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.8))
        popup.open()
    
    def open_payment_gateway(self):
        # This is where the payment gateway logic would go
        self.show_popup("Payment Gateway", "Payment gateway would be here.")

if __name__ == '__main__':
    MyApp().run()
