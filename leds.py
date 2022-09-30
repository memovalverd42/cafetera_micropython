from moduls.neopixel import Neopixel

class Leds:
    
    COLORS = {
        "apagado": (0, 0, 0),
        "verde":   (0, 255, 0),
        "rojo":    (255, 0, 0),
        "azul":    (0, 0, 255),
    }
    
    def init(self):
        NUM_PIX       = 8            
        NEOPIXELS_PIN = 27
        
        self.pixels = Neopixel(NUM_PIX, 0, NEOPIXELS_PIN, "GRB")    # Instancia de los neopixels
        self.pixels.fill(self.COLORS["apagado"])
        self.pixels.show()
        
    def off(self, index):
        self.pixels.set_pixel(index, self.COLORS["apagado"])
        self.pixels.show()

    def setColor(self, idx: int, color: str):
        self.pixels.set_pixel(idx, self.COLORS["apagado"])
        self.pixels.set_pixel(idx, self.COLORS[color])
        self.pixels.show()
        
    def toggle(self, idx, color, toggle):
        if toggle:
            self.pixels.set_pixel(idx, self.COLORS[color])
        else:
            self.pixels.set_pixel(idx, self.COLORS["apagado"])
        self.pixels.show()
    
        
        
        
        