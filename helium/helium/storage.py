from io import BytesIO

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont

class WatermarkStorage(FileSystemStorage):
    """
    为上传的图片增加水印并保存
    """
    def save(self, name, content, max_length=None):
        """保存逻辑"""
        if 'image' in content.content_type:
            # 加水印
            image = self.watermark_with_text(content, 'helium', 'red')
            content = self.convert_image_to_file(image, name)
        
        return super().save(name, content, max_length=max_length)
    
    def convert_image_to_file(self, image, name):
        """将图片对象转换为文件对象"""
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)
    
    def watermark_with_text(self, file_obj, text, color, fontfamily=None):
        """给图片打上水印"""
        image = Image.open(file_obj).convert('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            font = None
        textWidth, textHeight = draw.textsize(text, font)
        x = (width - textWidth - margin) / 2
        y = (height - textHeight - margin) / 2
        draw.text((x, y), text, color, font)
        return image