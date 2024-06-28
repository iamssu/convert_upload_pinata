import os
import json

# 이미지 다운로드 디렉토리 설정
download_dir = 'dir'
# 메타데이터 저장 디렉토리 설정
metadata_dir = 'metadata_dir'
os.makedirs(metadata_dir, exist_ok=True)

# 다운로드 디렉토리에서 이미지 파일 리스트 가져오기
image_files = [f for f in os.listdir(download_dir) if f.endswith('.jpg')]

# 각 이미지 파일에 대해 메타데이터 생성
for idx, image_file in enumerate(image_files, start=1):
    image_name = f'NAME_{str(idx).zfill(4)}'
    metadata = {
        "name": image_name,
        "description": "description",
        "external_url": None,
        "image": os.path.join(download_dir, image_file)
    }

    # 메타데이터 파일 저장
    metadata_filename = f'{image_name}.json'
    metadata_path = os.path.join(metadata_dir, metadata_filename)
    with open(metadata_path, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)
    
    print(f'메타데이터 저장 완료: {metadata_path}')
