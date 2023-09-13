from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import boto3
import botocore
from botocore.exceptions import NoCredentialsError
import os
import uvicorn

app = FastAPI()

# CORS 설정
origins = [
    "https://br-aipf.netlify.app",  # 클라이언트의 도메인을 여기에 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 필요한 HTTP 메서드를 여기에 추가
    allow_headers=["*"],  # 필요한 헤더를 여기에 추가
)

# AWS S3 설정
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

@app.post("/upload/")
async def upload_image(file: UploadFile):
    try:
        # 파일 이름 생성 (옵셔널)
        file_name = file.filename
        # S3에 이미지 업로드
        s3.upload_fileobj(file.file, AWS_BUCKET_NAME, file_name)
        s3_url = f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        return {"message": "이미지가 성공적으로 업로드되었습니다.", "s3_url": s3_url}
    except NoCredentialsError:
        return {"error": "AWS 자격 증명 오류"}
    except botocore.exceptions.ClientError as e:
        return {"error": str(e)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)