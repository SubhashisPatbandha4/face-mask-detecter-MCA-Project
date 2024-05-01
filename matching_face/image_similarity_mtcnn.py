import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import ImageEnhance
from PIL import Image


# Initialize MTCNN for face detection and alignment
mtcnn = MTCNN(keep_all=True)

# Initialize InceptionResnetV1 for face recognition
resnet = InceptionResnetV1(pretrained='vggface2').eval()

def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        if os.path.isfile(img_path):
            img = cv2.imread(img_path)
            if img is not None:
                images.append((filename, img))
    return images

def enhance_image(image):
    # Convert image to PIL format
    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Enhance brightness
    enhancer = ImageEnhance.Brightness(img_pil)
    img_pil = enhancer.enhance(1.5)
    
    # Convert back to OpenCV format
    enhanced_image = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    return enhanced_image

def extract_face_embeddings(img):
    # Enhance image to improve performance in low-light conditions
    img = enhance_image(img)
    
    # Convert image to RGB format (MTCNN requires RGB images)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect faces in the image
    faces = mtcnn(img_rgb)

    # Extract embeddings for each detected face
    embeddings = []
    for face in faces:
        if face is not None:
            # Resize face to the required input size of the face recognition model
            resized_face = cv2.resize(face.permute(1, 2, 0).numpy(), (96, 96))

            # Convert resized face to tensor
            resized_face_tensor = torch.tensor(resized_face.transpose(2, 0, 1), dtype=torch.float32)

            # Calculate embeddings using InceptionResnetV1
            embedding = resnet(resized_face_tensor.unsqueeze(0))

            # Append the embedding to the list
            embeddings.append(embedding.detach().numpy())

    return embeddings

def compare_image_with_folder(image_path, folder_path, threshold=0.6):
    # Load input image
    img = cv2.imread(image_path)

    # Extract face embeddings from input image
    input_embeddings = extract_face_embeddings(img)

    # Load images from the folder
    images = load_images_from_folder(folder_path)

    max_similarity = -1
    matched_image_path = None

    for filename, img in images:
        # Extract face embeddings from folder image
        folder_embeddings = extract_face_embeddings(img)

        # Compare input embeddings with folder embeddings
        for input_embedding in input_embeddings:
            for folder_embedding in folder_embeddings:
                similarity = cosine_similarity(input_embedding, folder_embedding)
                if similarity >= threshold and similarity > max_similarity:
                    max_similarity = similarity
                    matched_image_path = os.path.join(folder_path, filename)

    if matched_image_path is not None:
        print(f"Match found with highest similarity: {max_similarity[0][0]}")
        display_matched_images(image_path, matched_image_path)
    else:
        print("No match found.")

def display_matched_images(image_path1, image_path2):
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    # Resize images to have the same height
    height = min(img1.shape[0], img2.shape[0])
    img1 = cv2.resize(img1, (int(img1.shape[1] * height / img1.shape[0]), height))
    img2 = cv2.resize(img2, (int(img2.shape[1] * height / img2.shape[0]), height))

    # Concatenate images horizontally
    concatenated_img = np.concatenate((img1, img2), axis=1)

    # Display the concatenated image using Matplotlib
    plt.imshow(cv2.cvtColor(concatenated_img, cv2.COLOR_BGR2RGB))
    plt.title("Matched Images")
    plt.axis('off')
    plt.show()

def main():
    folder_path = r"D:\Web Development\Face_mask_detection-master\matching_face\student_images"

    # Prompt the user to input the path of the image to compare
    image_path = input("Enter the path of the image to compare: ")

    compare_image_with_folder(image_path, folder_path)

if __name__ == "__main__":
    main()
