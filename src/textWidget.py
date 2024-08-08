import pygame
import base64
from io import BytesIO
from PIL import Image
from colors import *

class textWidget(object):
    # Member vars same as menu pretty much
    border_color = base3
    title = pygame.font.init()
    title_text = "place holder"
    title_text_size = 40
    ScreenCoords = (0, 0)
    menu_width = 200
    menu_height = 200
    border_thickness = 0
    originalX = 0
    originalY = 0
    rect = pygame.Rect(ScreenCoords[0], ScreenCoords[1], menu_width, menu_height)
    image_surface = None  # To store the image surface

    def __init__(self, position: tuple[int, ...], width=200, height=200, inText="place holder"):
        pygame.font.init()  # Initialize font system
        self.ScreenCoords = position
        self.originalX = position[0]
        self.originalY = position[1]
        self.menu_width = width
        self.menu_height = height
        self.textCol = yellow
        self.border_thickness = 5
        self.border_color = base3
        self.image_surface = None
        
        # Define margins and areas
        self.text_area_height = height // 3
        self.image_area_height = height - self.text_area_height
        
        self.rect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], width, height)
        self.title_text = inText
        self.title_text_size = height // 6  # Adjusted text size for better fit
        self.title = pygame.font.Font(None, self.title_text_size)
        
        self.resizeBox(width, height)
        self.moveBox(position)

    def draw_rounded_rect(self, surface):
        inner_rect = self.rect.inflate(-4 * self.border_thickness, -4 * self.border_thickness)
        pygame.draw.rect(surface, null, inner_rect, 0, 20)  #hard setting the border radius as menus should be fixed "roundness"
        outer_rect = self.rect.inflate(self.border_thickness, self.border_thickness)
        pygame.draw.rect(surface, self.border_color, outer_rect, self.border_thickness, 20)

    def drawWidget(self, screen):
        # if self.border_thickness > 0:
        #     self.draw_rounded_rect(screen)
        
        # Draw the image if available
        if self.image_surface:
            image_rect = self.image_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - self.image_surface.get_height() // 2))
            screen.blit(self.image_surface, image_rect)
        
        # Render text with word wrap
        wrapped_lines = self.wrap_text(self.title_text, self.rect.width - self.border_thickness * 2)
        
        # Position text in the top area
        text_y = self.rect.top + self.border_thickness + 10
        for line in wrapped_lines:
            text_surf = self.title.render(line, True, self.textCol)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, text_y))
            screen.blit(text_surf, text_rect)
            text_y += text_rect.height + self.border_thickness + 10 # Move to the next line

    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            test_line = current_line + ' ' + word if current_line != '' else word
            test_size = self.title.size(test_line)
            
            if test_size[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines

    def changeTextSize(self, inSize):
        self.title = pygame.font.Font(None, inSize)
        self.title_text_size = inSize

    def resizeBox(self, width, height):
        self.rect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], width, height)
        self.menu_height = height
        self.menu_width = width
        self.text_area_height = height // 3
        self.image_area_height = height - self.text_area_height

    def moveBox(self, inPosition):
        self.rect.centerx = inPosition[0]
        self.rect.centery = inPosition[1]
        self.originalX = inPosition[0]
        self.originalY = inPosition[1]

    def updateText(self, inText):
        self.title_text = inText

    def set_image_from_base64(self, base64_str):
        if base64_str is None:
            self.image_surface = None
        else:
            # Decode the base64 string
            image_data = base64.b64decode(base64_str)
            image = Image.open(BytesIO(image_data))
            image = image.convert("RGBA")
            
            # Resize image to fit within widget dimensions
            original_width, original_height = image.size
            widget_width, widget_height = self.menu_width, self.image_area_height
            width_ratio = widget_width / original_width
            height_ratio = widget_height / original_height
            scale_ratio = min(width_ratio, height_ratio)
            new_width = int(original_width * scale_ratio)
            new_height = int(original_height * scale_ratio)
            image = image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert PIL image to Pygame surface
            image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
            self.image_surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
            self.image_surface.blit(image, (0, 0))