import requests
import os
import json  # json 모듈 import

# Pinata API 키 설정
PINATA_API_KEY = 'apikey'
PINATA_SECRET_API_KEY = 'secretkey'

# Pinata 업로드 함수
def upload_to_pinata(file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }
    with open(file_path, 'rb') as file:
        files = {
            'file': (os.path.basename(file_path), file)
        }
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            ipfs_hash = response.json()["IpfsHash"]
            print(f'Successfully uploaded {file_path} to IPFS: {ipfs_hash}')
            return ipfs_hash
        else:
            print(f'Failed to upload {file_path} to IPFS: {response.content}')
            return None

# 디렉토리 설정
download_dir = 'dir'
metadata_dir = 'metadata_dir'

# 이미지 파일 업로드
image_ipfs_hashes = {}
image_files = [f for f in os.listdir(download_dir) if f.endswith('.jpg')]
for image_file in image_files:
    image_path = os.path.join(download_dir, image_file)
    ipfs_hash = upload_to_pinata(image_path)
    if ipfs_hash:
        image_ipfs_hashes[image_file] = ipfs_hash

# 메타데이터 파일 업로드
metadata_files = [f for f in os.listdir(metadata_dir) if f.endswith('.json')]
for metadata_file in metadata_files:
    metadata_path = os.path.join(metadata_dir, metadata_file)
    
    # 메타데이터 파일 로드 및 이미지 IPFS 해시 추가
    with open(metadata_path, 'r') as file:
        metadata = json.load(file)
    image_file_name = os.path.basename(metadata['image'])
    if image_file_name in image_ipfs_hashes:
        metadata['image'] = f"ipfs://{image_ipfs_hashes[image_file_name]}"
    
    # 업데이트된 메타데이터 저장
    with open(metadata_path, 'w') as file:
        json.dump(metadata, file, indent=4)
    
    # 메타데이터 파일 업로드
    upload_to_pinata(metadata_path)
