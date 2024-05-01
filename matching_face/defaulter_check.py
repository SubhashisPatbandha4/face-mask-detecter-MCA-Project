import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import ImageEnhance
from PIL import Image
import json

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
    
     # Check if faces were detected
    if faces is None:
        return []

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

def main(threshold=0.6):
    # Set paths for the two image folders
    student_images_path = r"D:\Web Development\Face_mask_detection-master\matching_face\student_images"
    default_no_mask_images_path = r"D:\Web Development\Face_mask_detection-master\results\without_mask"

    # Load images from both folders
    student_images = load_images_from_folder(student_images_path)
    default_no_mask_images = load_images_from_folder(default_no_mask_images_path)

    # Initialize an empty dictionary to store student IDs and their match counts
    match_counts = {}

    # Compare each image in the default_no_mask_images folder with each image in the student_images folder
    for default_image_name, default_image in default_no_mask_images:
        for student_image_name, student_image in student_images:
            # Extract embeddings for the default image
            default_embeddings = extract_face_embeddings(default_image)

            # Extract embeddings for the student image
            student_embeddings = extract_face_embeddings(student_image)

            # Compare embeddings
            for default_embedding in default_embeddings:
                for student_embedding in student_embeddings:
                    similarity = cosine_similarity(default_embedding, student_embedding)
                    if similarity >= threshold:
                        # Extract student ID from the image name
                        student_id = int(student_image_name.split("_")[0])

                        # Update match count for this student ID
                        match_counts[student_id] = match_counts.get(student_id, 0) + 1

                        # Increment the default_mask value for this student ID by 1
                        # (Ensure it only increases once)
                        if match_counts[student_id] == 1:
                            # Load student database
                            student_database_path = "student_database.json"
                            with open(student_database_path, "r") as file:
                                student_database = json.load(file)

                            # Update default_mask value
                            student_database[str(student_id)]["default_mask"] = student_database.get(str(student_id), {"default_mask": 0})["default_mask"] + 1

                            # Save updated student database
                            with open(student_database_path, "w") as file:
                                json.dump(student_database, file, indent=4)

                            # Print message indicating database update
                            print(f"Default mask for Student ID {student_id} updated to {student_database[str(student_id)]['default_mask']}")

    # Print matched images and match accuracy
    for student_id, match_count in match_counts.items():
        print(f"Student ID {student_id}: {match_count} image(s) matched")

if __name__ == "__main__":
    main()
