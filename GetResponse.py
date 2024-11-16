from datetime import datetime
import csv




def get_response(user_input:str):
    lowered: str = user_input.lower()
    if 'collecte' in lowered and 'jus' in lowered :
        #TODO joindre le fichier
        return 'Voici le jus', True
    else :
        return 'kys',False