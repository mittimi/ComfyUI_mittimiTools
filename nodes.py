import torch
import comfy.sd
from comfy.cli_args import args
import folder_paths
import os
import re
import toml
import json


my_directory_path = os.path.dirname((os.path.abspath(__file__)))
presets_path_wh = os.path.join(my_directory_path, "presets/width_height/presets.toml")
preset_data_wh = ""
with open(presets_path_wh, 'r') as f:
    preset_data_wh = toml.load(f)
wh_list =  re.findall(r"\b\d+x\d+\b", preset_data_wh['wh'])



# ###################################################################
#  Input 
# ###################################################################


class WidthHeightMittimi:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "Width": ("INT", {"default": 512, "min": 1, "max": 2147483647} ),
                    "Height": ("INT", {"default": 512, "min": 1, "max": 2147483647} ),
                },
                "optional": {
                    "preset": (wh_list, ),
                },
                "hidden": {"node_id": "UNIQUE_ID" }
        }

    RETURN_TYPES = ("INT", "INT", )
    RETURN_NAMES = ("width", "height", )
    FUNCTION = "widthHeightMittimi"
    CATEGORY = "mittimiTools"

    def widthHeightMittimi(self, Width, Height, node_id, preset=[], ):
        return(Width, Height, )


class DaisyChainStringMittimi:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "add_first": ("STRING", ),
                "text": ("STRING", {"multiline": True}),
            },
            "optional": {
                "add_last": ("STRING", ),
            },
        }
    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("text", )
    FUNCTION = "daisyChainStringMittimi"
    CATEGORY = "mittimiTools"

    def daisyChainStringMittimi(self, text, add_first="", add_last="", ):

        return(add_first + text + add_last, )


# ###################################################################
#  IO 
# ###################################################################


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


# ###################################################################
#  Logic 
# ###################################################################


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
anytype = AnyType("*")


class AllowPassMittimi:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Pass": ("BOOLEAN", {"default": True}),
                "AnyData": (anytype,),
            },
        }

    RETURN_TYPES = (anytype,)
    RETURN_NAMES = ("AnyData",)
    FUNCTION = "allowPassMittimi"
    CATEGORY = "mittimiTools"

    def allowPassMittimi(self, Pass, AnyData):

        return_data = None
        if Pass:
            return_data = AnyData

        return (return_data, )


class CompareLengthsMittimi:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "Width": ("INT", {"default": 512, "min": 1, "max": 2147483647} ),
                    "Height": ("INT", {"default": 512, "min": 1, "max": 2147483647} ),
                },
        }

    RETURN_TYPES = ("INT", "INT", )
    RETURN_NAMES = ("long", "short", )
    FUNCTION = "compareLengthsMittimi"
    CATEGORY = "mittimiTools"

    def compareLengthsMittimi(self, Width, Height, ):
        longlength = Width
        shortlength = Height
        if (Height > Width):
            longlength = Height
            shortlength = Width
        return(longlength, shortlength, )





NODE_CLASS_MAPPINGS = {
    "WidthHeightMittimi": WidthHeightMittimi, 
    "DaisyChainStringMittimi": DaisyChainStringMittimi,
    "SaveLatentToInputFolderMittimi": SaveLatentToInputFolderMittimi, 
    "AllowPassMittimi": AllowPassMittimi, 
    "CompareLengthsMittimi": CompareLengthsMittimi, 
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "WidthHeightMittimi": "WidthHeight", 
    "DaisyChainStringMittimi": "DaisyChainString", 
    "SaveLatentToInputFolderMittimi": "SaveLatentToInputFolder", 
    "AllowPassMittimi": "AllowPass", 
    "CompareLengthsMittimi": "CompareLengths", 
}
