import consts
import face_recognition
import graphs
import json
import numpy as np
import os

gallery_path = consts.GALLERY_PATH
probe_path = consts.PROBES_PATH

GENUINE_PROBE_PATH = "genuine"
IMPOSTOR_PROBE_PATH = "impostors"

def generate_templates(dataset_path):
    templates_list = []
    identity_names = []
    for identity in os.listdir(dataset_path):
        identity_path = os.path.join(dataset_path, identity)
        for image in os.listdir(identity_path):
            image_path = os.path.join(identity_path, image)
            processed_image = face_recognition.load_image_file(image_path)
            encoded_faces = face_recognition.face_encodings(processed_image)
            if len(encoded_faces) > 1:
                print(f"More than one image was found in {image_path}")
                return
            if len(encoded_faces) < 0:
                print(f"No images were found in {image_path}")
                return
            templates_list.append(encoded_faces[0])
            identity_names.append(identity)

    return templates_list, identity_names

def distance_matrix_generator(gallery_path, probe_path):
    print("Generating enrolled users' templates . . .", end=" ")
    gallery_template_columns, gallery_identities = generate_templates(gallery_path)
    print("COMPLETED!")

    full_impostors_path = os.path.join(probe_path, "impostors")
    print("Generating probes' templates . . .", end=" ")
    impostor_template_rows, impostor_identities = generate_templates(full_impostors_path)
    
    full_genuine_path = os.path.join(probe_path, "genuine")
    genuine_template_rows, genuine_identities = generate_templates(full_genuine_path)

    probe_template_rows = genuine_template_rows + impostor_template_rows
    print("COMPLETED!")

    matrix = []
    print("Initiating the distances computations and distance matrix construction . . .", end=" ")
    for probe in probe_template_rows:
        matrix.append(face_recognition.face_distance(gallery_template_columns, probe).tolist())
    print("DONE!")
    hitchhikers = [gallery_identities, genuine_identities, impostor_identities]

    matrix.append(hitchhikers)
    #print(f"The matrix we created holds: \n{len(matrix)} rows!\n{len(matrix[0])} columns!\nThe number of identities in the rows are {len(matrix)/3}\nThe number of identities in the columns are {len(matrix[0])/3}")

    return matrix

def all_against_all(matrix, gallery_names, genuine_names, impostor_names):
    probe_names = genuine_names + impostor_names
    
    metrics = {}
    p_g = len(genuine_names)
    p_n = len(impostor_names)

    thresholds = [round(threshold, consts.ROUNDING_NUMBER) for threshold in np.arange(consts.MIN_THRESHOLD, consts.MAX_THRESHOLD, consts.THRESHOLD_STEP)] 

    for threshold in thresholds:
        metrics[threshold] = {
        "DI": 0,
        "GR": 0,
        "FR": 0,
        "FA": 0,
        }   
        for i, row in enumerate(matrix):
            rank_1_idx = row.index(min(row))
            matched_id = gallery_names[rank_1_idx]
            probe_id = probe_names[i]
            distance = float(row[rank_1_idx])

            if matched_id == probe_id:
                if distance < threshold:
                    metrics[threshold]["DI"] += 1
                else:
                    metrics[threshold]["FR"] += 1
                    
            elif probe_id in gallery_names:
                if not distance < threshold:
                    metrics[threshold]["FR"] += 1
            else:
                if distance < threshold:
                    metrics[threshold]["FA"] += 1 
                else:
                    metrics[threshold]["GR"] += 1

        metrics[threshold]["DIR"] = round(metrics[threshold]["DI"]/p_g, consts.ROUNDING_NUMBER)
        metrics[threshold]["FRR"] = round(1 - metrics[threshold]["DIR"], consts.ROUNDING_NUMBER)
        metrics[threshold]["FAR"] = round(metrics[threshold]["FA"]/p_n, consts.ROUNDING_NUMBER)
        metrics[threshold]["ERR"] = metrics[threshold]["FAR"] == metrics[threshold]["FRR"]

        #print(f"\t{threshold} -> {metrics[threshold]}")        
    return metrics

def main():  

    if not os.path.exists(consts.DISTANCE_MATRIX_NAME):
        print("No distance matrix previously found! Generating a new one. . .")
        matrix  = distance_matrix_generator(gallery_path, probe_path)
        with open(consts.DISTANCE_MATRIX_NAME, "w") as f_out:
            json.dump(matrix, f_out)
        
    else:
        print("An already existing distance matrix was found! Proceeding to use it . . .")
        with open(consts.DISTANCE_MATRIX_NAME, 'r') as f_in:
            matrix = json.load(f_in)
        
    
    
    gallery_names, genuine_names, impostor_names = matrix.pop()
    #print(f"The matrix holds: \n{len(matrix)} rows!\n{len(matrix[0])} columns!\nThe number of identities in the rows are {len(matrix)/3}\nThe number of identities in the columns are {len(matrix[0])/3}")    
    print("Computing evaluation metrics through all_against_all . . .")
    metrics = all_against_all(matrix, gallery_names, genuine_names, impostor_names)

    with open(consts.EVALUATION_METRICS_NAME, "w") as f_out:
        json.dump(metrics, f_out, indent=4)

    graphs.roc(metrics)
    graphs.det(metrics)
    graphs.eer(metrics)
    
main()

