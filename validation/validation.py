# import configparser
# import argparse
# import glob
# import os
# import logging

# # Logger configuration
# logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# logger = logging.getLogger(__name__)

# def validate_path_string(path, label):
#     errors = []

#     if not path.strip():
#         errors.append("path should not be empty")
#     if path != path.strip():
#         errors.append("path should not contain leading/trailing whitespace")
#     if "../imagelist" in path:
#         return True
#     if not os.path.exists(path):  
#         errors.append("path does not exist in the system")

#     if errors:
#         logger.error(f"Validation failed for {label} path: '{path}'")
#         for error in errors:
#             logger.error(f"- {error}")
#         return False
#     return True


# def validate_file_exists_string(file_name, label):
#     if not file_name.strip():
#         logger.error(f"Validation failed: No file present in {label}")
#         return False
#     return True


# def get_all_files_recursively(base_path):
#     return glob.glob(f"{base_path}/**", recursive=True)


# def validate_files_in_dir(file_names, directory_path, available_files, label):
#     for file_name in file_names:
#         full_path = f"{directory_path.rstrip('/')}/{file_name}"
#         if full_path in available_files:
#             logger.info(f"{label} file found: {full_path}")
#         else:
#             logger.error(f"{label} file NOT found in directory '{directory_path}': {file_name}")


# def validate_paths_inside_model_file(model_file_path):
#     logger.info(f"\n --- Validating Paths Inside [dataset]: {model_file_path.split('/')[-1]} ---")
#     is_valid = True
#     try:
#         with open(model_file_path, 'r') as file:
#             for line_num, line in enumerate(file, 1):
#                 line = line.strip()
#                 if not line:
#                     continue
#                 paths = [p.strip() for p in line.split(",") if p.strip()]
#                 for path in paths:
#                     label = f"line no - {line_num} \n"
#                     if not validate_path_string(path, label):
#                         is_valid = False
#     except Exception as e:
#         logger.error(f"Could not read model file '{model_file_path}': {e}")
#         is_valid = False

#     return is_valid


# def validate_config(config, config_file):
#     logger.info("**************************************************************")
#     logger.info(f"\n * Validating Configuration File: {config_file} * \n")
#     logger.info("************************************************************** \n")
#     is_valid = True

#     # === PATH SECTION ===
#     logger.info("\n --- Validating Paths in [path] section ---")
#     path_keys = ['input_dir', 'output_dir', 'tmp_dir', 'image_dir']
#     paths = {}

#     for key in path_keys:
#         if config.has_option('path', key):
#             value = config.get('path', key)
#             paths[key] = value
#             if not validate_path_string(value, key):
#                 is_valid = False
#         else:
#             logger.warning(f"'{key}' not found in [path] section")
#             is_valid = False
#     if is_valid:
#         logger.info("Paths validated successfully! \n")

#     input_dir = paths.get('input_dir', '')
#     image_dir = paths.get('image_dir', '')
#     if "../imagelist" in image_dir:
#         image_dir = image_dir.replace("../imagelist", "imagelist")

#     image_files = get_all_files_recursively(image_dir) if image_dir else []
#     input_files = get_all_files_recursively(input_dir) if input_dir else []

#     # === DATASET SECTION ===
#     logger.info("----------------------------------------------------------------------------")
#     logger.info("\n --- Validating Dataset Files in [dataset] section ---")
#     if config.has_option('dataset', 'calibration_set'):
#         calibration_set = config.get('dataset', 'calibration_set')
#         if validate_file_exists_string(calibration_set, "Calibration set"):
#             model_path1 = f"{image_dir.rstrip('/')}/{calibration_set}"
#             validate_files_in_dir([calibration_set], image_dir, image_files, "Calibration")
#             if not validate_paths_inside_model_file(model_path1):
#                 is_valid = False
#         else:
#             is_valid = False
#     else:
#         logger.warning("'calibration_set' not found in [dataset] section \n")

#     if config.has_option('dataset', 'validation_set'):
#         validation_set = config.get('dataset', 'validation_set')
#         if validate_file_exists_string(validation_set, "Validation set"):
#             model_path2 = f"{image_dir.rstrip('/')}/{validation_set}"
#             validate_files_in_dir([validation_set], image_dir, image_files, "Validation")
#             if not validate_paths_inside_model_file(model_path2):
#                 is_valid = False
#         else:
#             is_valid = False
#     else:
#         logger.warning("'validation_set' not found in [dataset] section \n")

#     # === NETWORK SECTION ===
#     logger.info("----------------------------------------------------------------------------")
#     logger.info("\n --- Validating Input Model File ---")
#     if config.has_option('network', 'input_model'):
#         input_model = config.get('network', 'input_model')
#         if validate_file_exists_string(input_model, "Input model"):
#             model_path = f"{input_dir.rstrip('/')}/{input_model}"
#             if model_path in input_files:
#                 logger.info(f"Input model file found: {model_path} \n")
#             else:
#                 logger.error(f"Input model file NOT found in directory '{input_dir}': {input_model} \n")
#         else:
#             is_valid = False
#     else:
#         logger.warning("'input_model' not found in [network] section")

#     return is_valid


# # === MAIN FUNCTION ===
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Validate .cfg configuration files.")
#     parser.add_argument("config_files", nargs='+', default="*.cfg",
#                         help="List of configuration files to validate")
#     args = parser.parse_args()

#     config_files = args.config_files

#     if not config_files:
#         logger.error(f"No .cfg files found matching the pattern: '{args.config_pattern}'")
#         exit(1)

#     all_valid = True
#     at_least_one_checked = False

#     for config_file in config_files:
#         config = configparser.ConfigParser()
#         try:
#             config.read(config_file)
#             if not config.sections():
#                 logger.warning(f"Configuration file '{config_file}' is empty or has no sections.")
#                 continue
#             at_least_one_checked = True
#             if not validate_config(config, config_file):
#                 all_valid = False
#         except configparser.Error as e:
#             logger.error(f"Error parsing configuration file '{config_file}': {e}")
#             all_valid = False



import configparser
import argparse
import glob
import os
import logging

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s:\n  %(message)s')
logger = logging.getLogger(__name__)


RELATIVE_IMAGE_PATH = "imagelist"
def validate_path_string(path, label):
    errors = []

    if not path.strip():
        errors.append("path should not be empty")
    if path != path.strip():
        errors.append("path should not contain leading/trailing whitespace")
    if "../imagelist" in path:
        return True
    if not os.path.exists(path):
        errors.append("path does not exist in the system \n")

    if errors:
        logger.error(f"Validation failed for {label} path: '{path}'")
        for error in errors:
            logger.error(f"- {error}")
        return False
    return True


def validate_file_exists_string(file_name, label):
    if not file_name.strip():
        logger.error(f"Validation failed:\n  No file present in {label}")
        return False
    return True


def get_all_files_recursively(base_path):
    return glob.glob(f"{base_path}/**", recursive=True)


def validate_files_in_dir(file_names, directory_path, available_files, label):
    for file_name in file_names:
        full_path = f"{directory_path.rstrip('/')}/{file_name}"
        if full_path in available_files:
            logger.info(f"{label} file found:\n  {full_path} \n")
        else:
            logger.error(f"{label} file NOT found in directory '{directory_path}':\n  {file_name}")


def validate_paths_inside_model_file(model_file_path):
    logger.info(f"--- Validating Paths Inside [dataset]: {model_file_path.split('/')[-1]} ---")
    is_valid = True
    try:
        with open(model_file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                paths = [p.strip() for p in line.split(",") if p.strip()]
                for path in paths:
                    label = f"line no - {line_num}"
                    if not validate_path_string(path, label):
                        is_valid = False
    except Exception as e:
        logger.error(f"Could not read model file '{model_file_path}':\n  {e}")
        is_valid = False

    return is_valid


def validate_config(config, config_file):
    logger.info(f"* Validating Configuration File: {config_file} *")
    is_valid = True

    # === PATH SECTION ===
    logger.info("--- Validating Paths in [path] section ---")
    path_keys = ['input_dir', 'output_dir', 'tmp_dir', 'image_dir']
    paths = {}

    for key in path_keys:
        if config.has_option('path', key):
            value = config.get('path', key)
            paths[key] = value
            if not validate_path_string(value, key):
                is_valid = False
        else:
            logger.warning(f"'{key}' not found in [path] section")
            is_valid = False
    if is_valid:
        logger.info("Paths validated successfully!\n")

    input_dir = paths.get('input_dir', '')
    image_dir = paths.get('image_dir', '')
    if "../imagelist" in image_dir:
        image_dir = image_dir.replace("../imagelist", RELATIVE_IMAGE_PATH)

    image_files = get_all_files_recursively(image_dir) if image_dir else []
    input_files = get_all_files_recursively(input_dir) if input_dir else []

    # === DATASET SECTION ===
    logger.info("--- Validating Dataset Files in [dataset] section ---")
    if config.has_option('dataset', 'calibration_set'):
        calibration_set = config.get('dataset', 'calibration_set')
        if validate_file_exists_string(calibration_set, "Calibration set"):
            model_path1 = f"{image_dir.rstrip('/')}/{calibration_set}"
            validate_files_in_dir([calibration_set], image_dir, image_files, "Calibration")
            if not validate_paths_inside_model_file(model_path1):
                is_valid = False
        else:
            is_valid = False
    else:
        logger.warning("'calibration_set' not found in [dataset] section\n")

    if config.has_option('dataset', 'validation_set'):
        validation_set = config.get('dataset', 'validation_set')
        if validate_file_exists_string(validation_set, "Validation set"):
            model_path2 = f"{image_dir.rstrip('/')}/{validation_set}"
            validate_files_in_dir([validation_set], image_dir, image_files, "Validation")
            if not validate_paths_inside_model_file(model_path2):
                is_valid = False
        else:
            is_valid = False
    else:
        logger.warning("'validation_set' not found in [dataset] section\n")

    # === NETWORK SECTION ===
    logger.info("--- Validating Input Model File ---")
    if config.has_option('network', 'input_model'):
        input_model = config.get('network', 'input_model')
        if validate_file_exists_string(input_model, "Input model"):
            model_path = f"{input_dir.rstrip('/')}/{input_model}"
            if model_path in input_files:
                logger.info(f"Input model file found:\n  {model_path}\n")
            else:
                logger.error(f"Input model file NOT found in directory '{input_dir}':\n  {input_model}\n")
        else:
            is_valid = False
    else:
        logger.warning("'input_model' not found in [network] section")

    return is_valid


# === MAIN FUNCTION ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate .cfg configuration files.")
    parser.add_argument("config_files", nargs='+', default="*.cfg",
                        help="List of configuration files to validate")
    args = parser.parse_args()

    config_files = args.config_files

    if not config_files:
        logger.error("No .cfg files found matching the given pattern.")
        exit(1)

    all_valid = True
    at_least_one_checked = False

    for config_file in config_files:
        config = configparser.ConfigParser()
        try:
            config.read(config_file)
            if not config.sections():
                logger.warning(f"Configuration file '{config_file}' is empty or has no sections.")
                continue
            at_least_one_checked = True
            if not validate_config(config, config_file):
                all_valid = False
        except configparser.Error as e:
            logger.error(f"Error parsing configuration file '{config_file}':\n  {e}")
            all_valid = False
