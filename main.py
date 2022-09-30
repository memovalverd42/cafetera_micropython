import machine, utime, ujson
from machine import Pin
from utime import sleep, ticks_ms, ticks_diff
from leds import Leds
import extra_functions as EF

led = Pin(3, Pin.OUT)   # Salida para control de dispensador
led.off()               # Estado inicial del dispensador

# Configuracion de valores para distinguir botones en el ADC
buttons = {
    "btn1": {
        "min": 63000,
        "max": 67000,
    },
    "btn2": {
        "min": 48000,
        "max": 53000,
    },
    "btn3": {
        "min": 37000,
        "max": 42000,
    },
    "btn4": {
        "min": 25000,
        "max": 29000,
    },
}

# Creación e iniciación de los Neopixeles
leds = Leds()
leds.init()

# Recuperar la configuracion de cada boton
conf_data = {}                                # Variable para guardar la configuración de cada boton
with open("data.json", "rb") as file:
    conf_data = ujson.load(file)

# Funcion para guardar data
def saveData(btn: str, time: int):
    #global conf_data
    conf_data[btn] = time                  # Guardado del tiempo en el objeto local
    with open('data.json', 'wb') as file:  # Guardado del objeto en data.json
        ujson.dump(conf_data, file)

# Función para dispensar café con respecto a la configuracíon almacenada
def dispense(option: str, idx: int):
    dispenser_timer_start = ticks_ms()
    blink_time_now = ticks_ms()
    led_state = True
    dispensing_time = conf_data[option]
    led.on()
    while True:
        if ticks_diff(ticks_ms(), blink_time_now) > 500:
            blink_time_now = ticks_ms()
            led_state = not led_state
            leds.toggle(idx, "verde", led_state)
            
        if ticks_diff(ticks_ms(), dispenser_timer_start) > dispensing_time:
            led.off()
            leds.off(idx)
            main()

# Funcion para configurar botones
def conf_mode(btn: str, idxBtn: int):
    sleep(1)
    min = buttons[btn]["min"]       # Valor limite inferior ADC del boton
    max = buttons[btn]["max"]       # Valor limite superior ADC del boton
    conf_state = True               # Variable para controlar el estado de la configuración                  
    bloq_btn   = True               # Variable para bloquear el multipulsado del boton
    led_state  = True
    blink      = False
    time_start_abort = ticks_ms()
    blink_time_now = ticks_ms()
    while True:
        
        # Si no sucede nada despues de 5 segundos, salimos del proceso hacia el main()
        if ticks_diff(ticks_ms(), time_start_abort) > 5000 and conf_state:
            print("Abortando...")
            leds.off(idxBtn)
            main()
            
        if ticks_diff(ticks_ms(), blink_time_now) > 200 and blink:
            blink_time_now = ticks_ms()
            led_state = not led_state
            leds.toggle(idxBtn, "rojo", led_state)
        
        # Si el boton se presiona
        if (min < EF.lectura_promedio() < max) and bloq_btn:
            # Si conf_state está en True, inicia la configuracíon...
            if conf_state:
                print("Configurando...")
                timer_start_conf = ticks_ms()  # Guardado de tiempo actual
                led.on()                       # Encendido del dispensador
                conf_state = False
                blink = True
            # Si conf_state es False, comienza el guardado del tiempo y regresar al main()
            else:
                print("Guardando...")
                led.off()                                                       # Apagado del dispensador
                timer_elapsed_conf = ticks_diff(ticks_ms(), timer_start_conf)   # Guardamos el tiempo de encendido
                conf_state = True                                               # Reseteamos variable conf_state
                saveData(btn, timer_elapsed_conf)                               # Mandamos la informacíon para el guardado
                leds.off(idxBtn)
                sleep(1)
                main()

        bloq_btn = False if (min < EF.lectura_promedio() < max) else True
        sleep(0.05)

# Función para gestionar los botones
def interrupcion(button: str, indexBtn):
    bloq = True
    min = buttons[button]["min"]     # Valor limite inferior ADC del boton
    max = buttons[button]["max"]     # Valor limite superior ADC del boton
    timer_start = ticks_ms()         # Guardado de tiempo actual

    # Si el boton se deja presionado...
    while (min < EF.lectura_promedio() < max):
        timer_elapsed = ticks_diff(ticks_ms(), timer_start)    # Diferencia de tiempo
        # Si el tiempo transcurrido (diferencia de tiempo) es mayor a 3 segundos...
        if (timer_elapsed) > 3000:
            leds.setColor(indexBtn, "rojo")                    # Encendemos led correspondiente en color rojo
            bloq = False
            conf_mode(button, indexBtn)                        # Entrar a modo de configuración
            
    # Si solo se realiza un pulso se activa el tiempo configurado para el boton...
    if bloq:
        leds.setColor(indexBtn, "verde")
        dispense(button, indexBtn)
        bloq = True

# Bucle principal
def main():
    while True:
        #reading = btn.read_u16()      
        #print("Lectura analogica = ", EF.lectura_promedio())
        
        if (buttons["btn1"]["min"] < EF.lectura_promedio() < buttons["btn1"]["max"]):
            pass
            interrupcion('btn1', 0)
        elif (buttons["btn2"]["min"] < EF.lectura_promedio() < buttons["btn2"]["max"]):
            pass
            interrupcion('btn2', 1)
        elif (buttons["btn3"]["min"] < EF.lectura_promedio() < buttons["btn3"]["max"]):
            pass
            interrupcion('btn3', 2)
        elif (buttons["btn4"]["min"] < EF.lectura_promedio() < buttons["btn4"]["max"]):
            pass
            interrupcion('btn4', 3)
            
        sleep(0.1)

if __name__ == "__main__":
    main()
