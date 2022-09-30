from machine import ADC



# Función que calcula el promedio de 15 lecturas en el ADC
ADC_PIN = 28
btn = ADC(28)                    # Pin 28 como entrada analogica
def lectura_promedio() -> int:
    total = 0
    count = 0
    while count < 20:
        reading = btn.read_u16() 
        total += reading
        count += 1
    return int(total/20) 