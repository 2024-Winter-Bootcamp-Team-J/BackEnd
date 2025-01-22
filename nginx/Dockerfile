# Nginx 이미지 기반으로 시작
FROM nginx:latest

RUN apt-get update  && apt-get install -y nginx


# Nginx 설정 파일 복사
COPY ./nginx.conf /etc/nginx/nginx.conf
#COPY nginx.conf /etc/nginx/nginx.conf

# 포트 노출
EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]