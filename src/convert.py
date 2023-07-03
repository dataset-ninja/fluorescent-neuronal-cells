import glob
import os
import shutil
from urllib.parse import unquote, urlparse
from cv2 import connectedComponents

import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_name
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_ds_path: str) -> str:
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    file_info = api.file.get_info_by_path(team_id, teamfiles_ds_path)
    file_name_with_ext = file_info.name
    local_path = os.path.join(storage_dir, file_name_with_ext)
    dataset_path = os.path.splitext(local_path)[0]

    if not os.path.exists(dataset_path):
        sly.logger.info(f"Dataset dir '{dataset_path}' does not exist.")
        if not os.path.exists(local_path):
            sly.logger.info(f"Downloading archive '{teamfiles_ds_path}'...")
            api.file.download(team_id, teamfiles_ds_path, local_path)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        path = unpack_if_archive(local_path)
        sly.logger.info(f"Archive '{file_name_with_ext}' was unpacked successfully to: '{path}'.")
        sly.logger.info(f"Dataset dir contains: '{os.listdir(path)}'.")
        sly.fs.silent_remove(local_path)

    else:
        sly.logger.info(
            f"Archive '{file_name_with_ext}' was already unpacked to '{dataset_path}'. Skipping..."
        )
    return dataset_path


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    dataset_path = "/Users/almaz/Downloads/FluorescentNeuronalCells"
    anns_folder = "ann"
    images_folder = "img"
    batch_size = 30

    def create_ann(image_path):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        image_name = os.path.basename(image_path)
        mask_path = os.path.join(anns_path, image_name)

        if sly.fs.file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            unique_pixels = np.unique(mask_np)[1:]
            for curr_pixel in unique_pixels:
                mask = mask_np == curr_pixel
                ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
                for i in range(1, ret):
                    obj_mask = curr_mask == i
                    curr_bitmap = sly.Bitmap(obj_mask)
                    curr_label = sly.Label(curr_bitmap, obj_class)
                    labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    obj_class = sly.ObjClass("stained neuron", sly.Bitmap)

    project = api.project.create(workspace_id, project_name)
    meta = sly.ProjectMeta(obj_classes=[obj_class])
    api.project.update_meta(project.id, meta.to_json())

    ds_name = "ds0"
    dataset = api.dataset.create(project.id, ds_name)

    images_path = os.path.join(dataset_path, images_folder)
    anns_path = os.path.join(dataset_path, anns_folder)

    images_names = os.listdir(images_path)

    progress = tqdm(desc=f"Create dataset {ds_name}", total=len(images_names))

    for img_names_batch in sly.batched(images_names, batch_size=batch_size):
        img_pathes_batch = [os.path.join(images_path, path) for path in img_names_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.update(len(img_names_batch))

    # sly.logger.info('Deleting temporary app storage files...')
    # shutil.rmtree(dataset_path)

    return project
