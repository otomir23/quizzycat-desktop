[Пояснительная записка](NOTE.md)

# quizzycat Desktop

This is a desktop application for the [quizzycat](https://quizzycat.vercel.app/) web app.

Made using **PyQt5** for **Yandex Academy Lyceum 2022**. 

The code isn't as good as I would like it to be, 
but I had to finish it in a week, so I had to make some compromises.

## Installation

Download latest executable for your OS from 
[releases](https://github.com/otomir23/quizzycat-desktop/releases).

## Running from source

### Setup

#### Windows:

```shell
git clone https://github.com/otomir23/quizzycat-desktop.git
cd quizzycat-desktop
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### MacOS/Linux:

```bash 
git clone https://github.com/otomir23/quizzycat-desktop.git
cd quizzycat-desktop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run

```shell
python main.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
