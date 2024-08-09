import pygame
import base64
from io import BytesIO
from PIL import Image as PILImage

class Base64Image:
    def __init__(self, base64_string, max_width=300, max_height=250):
        self.base64_string = base64_string
        self.max_width = max_width
        self.max_height = max_height
        self.image = None
        self.load_image()

    def load_image(self):
        # Decode the base64 string
        if self.base64_string:
            image_data = base64.b64decode(self.base64_string)
            # Convert the binary data to a PIL image
            pil_image = PILImage.open(BytesIO(image_data))

            # Get original dimensions
            original_width, original_height = pil_image.size
            
            # Calculate the scaling factors and new dimensions
            width_scale = self.max_width / original_width
            height_scale = self.max_height / original_height
            scale = min(width_scale, height_scale)
            
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            # Resize image while maintaining aspect ratio
            pil_image = pil_image.resize(
                (new_width, new_height), PILImage.Resampling.LANCZOS
            )
            
            # Convert the PIL image to a Pygame surface
            self.image = pygame.image.fromstring(
                pil_image.tobytes(), pil_image.size, pil_image.mode
            )

    def drawImage(self, surface, x, y):
        if self.image:
            surface.blit(self.image, (x, y))
