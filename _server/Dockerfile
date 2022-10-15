FROM python:latest

RUN mkdir /server_interface

ADD ../requirements.txt /server_interface
ADD ../server.py /server_interface
ADD ../config.py /server_interface
ADD ../image_utils.py /server_interface
ADD ../proto /server_interface/proto

#ADD ../image_pb2.py /server_interface
#ADD ../image_pb2_grpc.py /server_interface

ADD ../_server/run_server.sh /server_interface
ADD ../setup /server_interface
ADD ../build /server_interface
ADD ../server /server_interface

WORKDIR /server_interface

RUN apt-get update
RUN apt-get install libgl1 -y
#RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

# Build grpc scripts
RUN python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/image.proto

RUN chmod +x run_server.sh

#CMD [ "python", "server.py", "--port", "23333", "--host", "127.0.0.1"]
ENTRYPOINT ["/server_interface/run_server.sh"]
