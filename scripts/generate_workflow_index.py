import json
import os


def generate_index():
    workflows_dir = "workflows"
    index_file = "workflows/index.json"

    # Base URL for raw content
    base_url = (
        "https://raw.githubusercontent.com/SNL-UCSB/netgent-workflow/main/workflows/"
    )

    workflows_list = []

    # Iterate through each folder in the workflows directory
    for folder_name in sorted(os.listdir(workflows_dir)):
        folder_path = os.path.join(workflows_dir, folder_name)

        # We only care about directories that contain a manifest.json
        if os.path.isdir(folder_path):
            manifest_path = os.path.join(folder_path, "manifest.json")

            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, "r") as f:
                        manifest = json.load(f)

                        # Use the "main" entry from manifest, or default to workflow.json
                        main_file = manifest.get("main", "workflow.json")

                        workflows_list.append(
                            {
                                "id": folder_name,
                                "name": manifest.get(
                                    "name", folder_name.replace("_", " ").title()
                                ),
                                "description": manifest.get(
                                    "description", "No description provided."
                                ),
                                "version": manifest.get("version", "1.0.0"),
                                "workflowlink": f"{base_url}{folder_name}/{main_file}",
                            }
                        )
                except Exception as e:
                    print(f"Error processing {folder_name}: {e}")

    with open(index_file, "w") as f:
        json.dump(workflows_list, f, indent=2)
    print(f"Successfully generated {index_file} with {len(workflows_list)} workflows.")


if __name__ == "__main__":
    generate_index()
