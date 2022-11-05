from db.models import User
from page import Page


class AuthPage(Page):
    def initUI(self):
        super().initUI('pages/auth.ui')
        self.loginButton.clicked.connect(self.login)

    def login(self):
        self.errorLabel.setText('')

        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if not username or not password:
            self.errorLabel.setText('Username and password are required')
            return

        user = User.select().where(User.username == username).first()

        if not user:
            self.errorLabel.setText('User not found')
            return

        if not user.checkPassword(password):
            self.errorLabel.setText('Incorrect password')
            return

        print('Logged in as', user.name, user.surname)
