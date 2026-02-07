import torch
import comfy.sd
from comfy.cli_args import args
import folder_paths
import os
import json


class SaveLatentToInputFolderMittimi:

    SEARCH_ALIASES = ["export latent"]

    def __init__(self):
        self.output_dir = folder_paths.get_input_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {"optional": { "samples": ("LATENT", ),
                              "filename_prefix": ("STRING", {"default": "latents/ComfyUI"})},
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }
    RETURN_TYPES = ()
    FUNCTION = "saveLatentToInputFolderMittimi"
    OUTPUT_NODE = True
    CATEGORY = "mittimiTools"

    def saveLatentToInputFolderMittimi(self, samples=None, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):

        if samples is None:
            return()

        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)

        # support save metadata for latent sharing
        prompt_info = ""
        if prompt is not None:
            prompt_info = json.dumps(prompt)

        metadata = None
        if not args.disable_metadata:
            metadata = {"prompt": prompt_info}
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata[x] = json.dumps(extra_pnginfo[x])

        file = f"{filename}_{counter:05}_.latent"

        results: list[FileLocator] = []
        results.append({
            "filename": file,
            "subfolder": subfolder,
            "type": "output"
        })

        file = os.path.join(full_output_folder, file)

        output = {}
        output["latent_tensor"] = samples["samples"].contiguous()
        output["latent_format_version_0"] = torch.tensor([])

        comfy.utils.save_torch_file(output, file, metadata=metadata)
        return { "ui": { "latents": results } }






NODE_CLASS_MAPPINGS = {
    "SaveLatentToInputFolderMittimi": SaveLatentToInputFolderMittimi, 
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveLatentToInputFolderMittimi": "SaveLatentToInputFolder", 
}
