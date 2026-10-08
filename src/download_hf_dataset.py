from huggingface_hub import snapshot_download
local = snapshot_download(repo_id="lerobot/robomme", repo_type="dataset")
print(f"Dữ liệu đã được tải về thư mục: {local}")
