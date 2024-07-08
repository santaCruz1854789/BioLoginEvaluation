import os 
import shutil
import consts

tot_ids = consts.TOTAL_IDENTITIES
gen_ids = consts.ENROLLED_IDENTITIES
imp_ids = consts.IMPOSTORS_IDENTITES

src_dir = "./CASIA_WebFace_dataset"

id_dirs_relative = os.listdir(src_dir)
id_dirs = [os.path.join(src_dir, src) for src in id_dirs_relative]

gallery = "Eval_Dataset/gallery"
genuine = "Eval_Dataset/probes/genuine"
impostors = "Eval_Dataset/probes/impostors"
os.makedirs(gallery, exist_ok=True)
os.makedirs(genuine, exist_ok=True)
os.makedirs(impostors, exist_ok=True)

f_num = lambda x: x.split("_")[-1]

for i in range(gen_ids):
    
    for template in os.listdir(id_dirs[i])[:consts.ENROLLED_TEMPLATES]:
        gallery_dst_id = os.path.join(gallery, id_dirs_relative[i])
        if not os.path.exists(gallery_dst_id):
            os.makedirs(gallery_dst_id)
        
        new_name = f"template_{f_num(template)}"
        shutil.copy(os.path.join(id_dirs[i], template), os.path.join(gallery_dst_id, new_name))

    for probe in os.listdir(id_dirs[i])[consts.ENROLLED_TEMPLATES:consts.ENROLLED_TEMPLATES+ consts.PROBES_ATTEMPTS]:
        probe_dst_id = os.path.join(genuine, id_dirs_relative[i])
        if not os.path.exists(probe_dst_id):
            os.makedirs(probe_dst_id)

        new_name = f"genuine_{f_num(probe)}"
        shutil.copy(os.path.join(id_dirs[i], probe), os.path.join(probe_dst_id, new_name))

for i in range(gen_ids, tot_ids):
    for impostor in os.listdir(id_dirs[i])[:consts.PROBES_ATTEMPTS]:
        probe_dst_id = os.path.join(impostors, id_dirs_relative[i])
        if not os.path.exists(probe_dst_id):
            os.makedirs(probe_dst_id)
        
        new_name = f"impostor_{f_num(impostor)}"
        shutil.copy(os.path.join(id_dirs[i], impostor), os.path.join(probe_dst_id, new_name))