from tinydb import TinyDB

# פונקציה לשמירת מידע במסדי נתונים
def save_to_db(which_plant, tags_data, lyout, invalid_lyout):
    try:
        TAGS_DB = TinyDB(f'./DB/TAGS_DB_{which_plant}.json')
        LYOUT_DB = TinyDB(f'./DB/LYOUT_DB_{which_plant}.json')
        Invalid_LYOUT_DB = TinyDB(f'./DB/Invalid_LYOUT_DB_{which_plant}.json')

        # מנקה ומכניס את הנתונים למסדי הנתונים
        TAGS_DB.truncate()
        TAGS_DB.insert({which_plant: tags_data})

        LYOUT_DB.truncate()
        LYOUT_DB.insert(lyout)

        Invalid_LYOUT_DB.truncate()
        Invalid_LYOUT_DB.insert(invalid_lyout)
        # סגירת מסדי הנתונים
        TAGS_DB.close()
        LYOUT_DB.close()
        Invalid_LYOUT_DB.close()

    except Exception as e:
        print(e)
        print("ERROR IN PMs")