FROM python:latest

RUN mkdir /client_interface

ADD ../requirements.txt /client_interface
ADD ../client.py /client_interface
ADD ../config.py /client_interface
ADD ../image_utils.py /client_interface

ADD ../proto /client_interface/proto
ADD ../images /client_interface/images

#ADD ../image_pb2.py /client_interface
#ADD ../image_pb2_grpc.py /client_interface

ADD ../_client/run_client.sh /client_interface
ADD ../setup /client_interface
ADD ../build /client_interface
ADD ../client /client_interface

WORKDIR /client_interface

RUN apt-get update
RUN apt-get install libgl1 -y
#RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

# Build grpc scripts
RUN python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/image.proto

RUN chmod +x run_client.sh

#CMD [ "python", "server.py", "--port", "23333", "--host", "127.0.0.1"]
ENTRYPOINT ["/client_interface/run_client.sh"]
