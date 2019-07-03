## Application for relief distribution

### To run the app in dev mode

- Install python3 and pipenv
- run the following commands in the root directory

```bash
    pipenv install
```

```bash
    pipenv run python3 main.py
```

- If running on windows 
```bash
    pipenv run python main.py
```

### To build the app

- Install all the dependencies before continuing
- Then run the following command in the root of the project

```bash
    pyinstaller main.py --onefile
```
- The executable will be then found in `dist` directory.