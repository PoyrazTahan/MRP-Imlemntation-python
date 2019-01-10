from InfoProject import App

def main():
    database_file = "MrpDB.db"
    app = App(database_file)
    app.start()

if __name__ == '__main__':
    main()