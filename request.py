import os
import socket
from datetime import datetime
class SocketServer:
    def __init__(self):
        self.bufsize = 1024 # 버퍼 크기 설정
        with open('./response.bin', 'rb') as file:
            self.RESPONSE = file.read() # 응답 파일 읽기
        self.DIR_PATH = './request'
        self.createDir(self.DIR_PATH)
    def createDir(self, path):
        """디렉토리 생성"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error: Failed to create the directory.")
    def run(self, ip, port):
        """서버 실행"""
        # 소켓 생성
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(10)
        print("Start the socket server...")
        print("\"Ctrl+C\" for stopping the server!\r\n")
        try:
            while True:
                # 클라이언트의 요청 대기
                clnt_sock, req_addr = self.sock.accept()
                clnt_sock.settimeout(10.0) # 타임아웃 설정(5초)
                print("Request message...\r\n")
                response = b""
                # 여기에 구현 하세요
                data = clnt_sock.recv(40000)
                now = datetime.now()
                reqeustDate = now.strftime("%Y-%m-%d-%H-%M-%S")
                requestFile = open("./request/"+reqeustDate+".bin","wb")
                requestFile.write(data)
                requestFile.close()
                imageFile = open("./request/"+reqeustDate+".jpg","wb")
                
                count = 0
                boundaryLength = 0
                imageLength = 0
                for i in data:
                    
                    if count>=8 and (data[count-8], data[count-7], data[count-6],data[count-5],data[count-4],data[count-3],data[count-2],data[count-1],data[count]) == (0x62, 0x6f, 0x75, 0x6e, 0x64, 0x61, 0x72, 0x79, 0x3d):
                        
                        boundary = []
                        while(data[count+boundaryLength+1]!=0x0d):
                            boundary.append(data[count+boundaryLength+1])
                            boundaryLength+=1
                        print(boundary)
                        break
                    count+=1
                count =0
                for i in data:
                    
                    if count >=12 and (data[count-12], data[count-11], data[count-10],data[count-9],data[count-8],data[count-7],data[count-6],data[count-5],data[count-4],data[count-3],data[count-2],data[count-1],data[count])==(0x69 , 0x6d, 0x61, 0x67, 0x65, 0x2f, 0x6a, 0x70, 0x67, 0x0d, 0x0a, 0x0d, 0x0a):
                        print("image found")
                        writing = True
                        while(writing):
                            if (data[count+imageLength+1], data[count+imageLength+2],data[count+imageLength+3], data[count+imageLength+4]) == (0x0d, 0x0a, 0x2d, 0x2d):
                                boundaryCheckCount = 0
                                writing = False
                                while boundaryCheckCount <boundaryLength:
                                    if data[count+imageLength+5+boundaryCheckCount] != boundary[boundaryCheckCount]:
                                        writing = True
                                    boundaryCheckCount+=1
                                if writing == False:
                                    imageFile.write(data[count+1:count+imageLength+1])
                            if writing:
                                imageLength+=1
                        break
                    count+=1
                    
                imageFile.close()   
                print("이미지 처리 완료")
                # 응답 전송
                clnt_sock.sendall(self.RESPONSE)
                # 클라이언트 소켓 닫기
                clnt_sock.close()
        except KeyboardInterrupt:
            print("\r\nStop the server...")
            # 서버 소켓 닫기
        self.sock.close()
if __name__ == "__main__":
    server = SocketServer()
    server.run("127.0.0.1",8000)