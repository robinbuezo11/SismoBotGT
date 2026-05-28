import re

def detect_intent(message: str):
    msg = message.lower()

    patrones_sismos = [ 
        r"\bsismo\b", 
        r"\bsismos\b", 
        r"\btemblor\b", 
        r"\btemblores\b", 
        r"\bterremoto\b", 
        r"\bactividad sísmica\b", 
        r"\bactividad sismica\b", 
        r"\bmovimiento telúrico\b", 
        r"\bmovimiento telurico\b", 
    ]

    for patron in patrones_sismos:
        if re.search(patron, msg):
            return "consulta_sismos"
            
    return "general"