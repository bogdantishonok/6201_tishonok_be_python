from dotenv import load_dotenv
import os
import requests
import numpy as np
from PIL import Image
import scipy.ndimage
import matplotlib.pyplot as plt

load_dotenv()
api_key = os.getenv('api_key')
headers = {'x-api-key': api_key}
url = os.getenv('url')

try:
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    response_dict = r.json()

    if not response_dict or 'breeds' not in response_dict[0] or not response_dict[0]['breeds']:
        print("Ошибка: Не удалось получить данные о породе или изображении.")
        exit()

    breed = response_dict[0]['breeds'][0]['name']
    image_url = response_dict[0]['url']

    image_response = requests.get(image_url)
    image_response.raise_for_status()
    image = Image.open(requests.get(image_url, stream=True).raw)

except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к API: {e}")
    exit()
except Exception as e:
    print(f"Произошла ошибка: {e}")
    exit()

def manual_convolution(image_array, kernel):
    kernel_height, kernel_width = kernel.shape
    padded_image = np.pad(image_array, ((kernel_height // 2, kernel_height // 2),
                                         (kernel_width // 2, kernel_width // 2),
                                         (0, 0)), mode='constant')
    output = np.zeros_like(image_array)

    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            for k in range(image_array.shape[2]):
                output[i, j, k] = np.sum(padded_image[i:i + kernel_height, j:j + kernel_width, k] * kernel)

    return output

def scipy_convolution(image_array, kernel):
    output = np.zeros_like(image_array)
    for i in range(image_array.shape[2]):  # Для каждого канала RGB
        output[..., i] = scipy.ndimage.convolve(image_array[..., i], kernel)
    return output

try:
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(image)
    plt.axis('off')
    plt.title(f'{breed.capitalize()}')

    image_array = np.array(image)

    print(f"Image shape: {image_array.shape}")

    kernel = np.ones((3, 3)) / 9.0

    print(f"Kernel shape: {kernel.shape}")

    manual_output = manual_convolution(image_array, kernel)

    scipy_output = scipy_convolution(image_array, kernel)

    plt.subplot(1, 3, 2)
    plt.imshow(manual_output.astype(np.uint8))
    plt.axis('off')
    plt.title(f'Manual Convolution\n{breed.capitalize()}')

    plt.subplot(1, 3, 3)
    plt.imshow(scipy_output.astype(np.uint8))
    plt.axis('off')
    plt.title(f'SciPy Convolution\n{breed.capitalize()}')

    plt.tight_layout()
    plt.show()

    image.save(f'{breed}_original.png')
    Image.fromarray(manual_output.astype(np.uint8)).save(f'{breed}_manual_convolution.png')
    Image.fromarray(scipy_output.astype(np.uint8)).save(f'{breed}_scipy_convolution.png')

except Exception as e:
    print(f"Произошла ошибка при обработке изображения: {e}")