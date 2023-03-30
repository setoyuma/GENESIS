class ColorGradient:
    def __init__(self, init_color, target_color):
        # Init color fade vars
        self.steps = 200
        self.color = init_color
        self.colorFrom = list(init_color)
        self.colorTo = list(target_color)
        self.inv_steps = 1.0 / self.steps
        self.step_R = (self.colorTo[0] - self.colorFrom[0]) * self.inv_steps
        self.step_G = (self.colorTo[1] - self.colorFrom[1]) * self.inv_steps
        self.step_B = (self.colorTo[2] - self.colorFrom[2]) * self.inv_steps
        self.r = self.colorFrom[0]
        self.g = self.colorFrom[1]
        self.b = self.colorFrom[2]
        self.target_reached = False

    def calc_steps(self, colorTo):
        self.colorFrom = self.color
        self.colorTo = colorTo
        self.step_R = (self.colorTo[0] - self.colorFrom[0]) * self.inv_steps
        self.step_G = (self.colorTo[1] - self.colorFrom[1]) * self.inv_steps
        self.step_B = (self.colorTo[2] - self.colorFrom[2]) * self.inv_steps

    def next(self):
        self.r += self.step_R
        self.g += self.step_G
        self.b += self.step_B
        self.color = (int(self.r), int(self.g), int(self.b))

        # check if target has been reached
        if all([(self.step_R >= 0 and self.r >= self.colorTo[0]) or (self.step_R <= 0 and self.r <= self.colorTo[0]),
            (self.step_G >= 0 and self.g >= self.colorTo[1]) or (self.step_G <= 0 and self.g <= self.colorTo[1]),
            (self.step_B >= 0 and self.b >= self.colorTo[2]) or (self.step_B <= 0 and self.b <= self.colorTo[2])]):
            self.target_reached = True
        
        return self.color

    """ 
    Returns a list of all the colors in between the 
    initial color and target color 
    """
    def generate_gradient(self):
        gradient = []
        while not self.target_reached:
            gradient.append(self.next())
        print(gradient)
        return gradient