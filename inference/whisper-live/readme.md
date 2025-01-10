# Deploy Whisper Live on TIR

#### Server Configuration Steps:
1. In TIR, create a new node with a GPU of your choice: H100 or H200 
2. After node comes to a running state, go to `Network & Security` tab and add a new application TCP port - 9090. Wait for a few seconds and refresh the section to see new public ip being assigned to your node. We will need this public IP when connecting to the service from client so copy it to a notepad or text editor on your laptop
3. Now, click on the jupyter labs icon for your node, this will open up jupyter labs.
<img width="1211" alt="node" src="https://github.com/user-attachments/assets/d06fc8f6-f4ca-44fd-9b08-1414a185f3b2" />

4. Once you are in jupyter labs, open a new terminal
5. Clone the Whisper-Live repo:
   ```
     git clone https://github.com/collabora/WhisperLive
     cd WhisperLive
   ```
6. Run these commands to install dependencies: 
   ```
   $ apt update && apt install -y python3-pip python3.12-venv portaudio19-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
   $ python3 -m venv whisper-env
   $ /home/jovyan/WhisperLive/whisper-env/bin/activate 
   $ pip install --no-cache-dir -r requirements/server.txt
   
   ```
7. Run the server now. Wait for a while at first run, as the model gets downloaded 
   ```
     python3 run_server.py --port 9090  
   ```

#### Setup Client on your laptop:
1. Open terminal
2. Clone whisper-live repo
   ```
     git clone https://github.com/collabora/WhisperLive
     cd WhisperLive
   ```
3. Install dependencies:
   ```
     $ brew install portaudio
     $ pip install -r requirements/client.txt 
   ```
4. Open python3 cli:
   ```
   $ python3
   ```
5. Run the following code to connect with the server and test:
   ```
      from whisper_live.client import TranscriptionClient
      client = TranscriptionClient(
               "216.48.189.92",
               9090,
               lang="en",
               translate=False,
               use_vad=False,
               max_clients=4,
               max_connection_time=600)
       client("test/xyz.wav")  # use a valid file path or use mic if your terminal allows 
   ```
6. If all goes well, you will start seeing the transcription the terminal. 
