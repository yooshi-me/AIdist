from tensorflow.keras.datasets import cifar10
from pathlib import Path
from PIL import Image

(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

output_dir = Path("data/cifar-10/test")

labels = ["airplane","automobile","bird","cat","deer","dog","frog","horse","ship","truck"]

for i, (img, label) in enumerate(zip(train_images, train_labels)):
    save_dir = output_dir / labels[int(label[0])]
    save_dir.mkdir(exist_ok=True, parents=True)
    save_path = save_dir / f"{i}.png"

    img = Image.fromarray(img)
    img.save(save_path)