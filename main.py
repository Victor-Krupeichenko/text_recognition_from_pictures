import os
import easyocr


class TextRecognition:
    """
    Класс для распознавания текста с изображения
    """

    def __init__(self, path_image_folder, number_image=1, language='en', multilingual=False, threshold=0.25):
        """
        Конструктор класса
        :param path_image_folder: Путь к папке с изображениями
        :param number_image: номер изображения которое нужно загрузить (по умолчанию первое изображение)
        :param language: язык для распознавания текста(по умолчанию английский)
        :param multilingual: мультиязычность (по умолчанию False)
        :param threshold: порог распознавания текста(по умолчанию 0.25)
        """
        self.path_image_folder = path_image_folder
        self.number_image = number_image
        if multilingual:
            self.language = ['en', 'ru']
        else:
            self.language = [language]
        self.threshold = threshold
        self.image_name = None
        self.text = None

    def get_image(self):
        """
        Получает изображение по указанному пути
        :return: возвращает полный путь к изображению
        """
        for num, image_name in enumerate(os.listdir(self.path_image_folder), start=1):
            if num == self.number_image:
                return f'{self.path_image_folder}/{image_name}'
        return False

    def get_text_from_image(self, image, paragraph=False):
        """
        Получает текст из изображения
        :param image: путь к изображению
        :param paragraph: показывать ли параграфы(по умолчанию не показывать)
        :return: возвращает текст изображения
        """
        reader = easyocr.Reader(self.language)
        temp_text = reader.readtext(image, paragraph=paragraph)
        text = []
        if temp_text:
            for _, row, score in temp_text:
                if score >= self.threshold:
                    text.append(row)
            return text
        return False

    def save_text_to_file(self, image_name, text):
        """
        Сохраняет текст изображения в файл с названием изображения
        :param image_name: имя изображения
        :param text: текст изображения
        """
        with open(f'{image_name}.txt', 'w', encoding='utf8') as file:
            file.writelines(f'{line}\n' for line in text)

    def main(self):
        """
        Основной метод в котором вызываются все необходимые для работы этой программы методы
        """
        image = self.get_image()
        if image:
            self.image_name = os.path.basename(image).split('.')[0]
            self.text = self.get_text_from_image(image)
        if self.text:
            self.save_text_to_file(self.image_name, self.text)
        else:
            text = [f'В {self.image_name} - Не удалось найти или распознать текст']
            self.save_text_to_file(self.image_name, text)


if __name__ == '__main__':
    path_folder = 'test_images'
    text_recognition = TextRecognition(path_image_folder=path_folder, number_image=6, multilingual=True)
    text_recognition.main()
