import math
import os
import librosa
from lyzr import VoiceBot
from dotenv import load_dotenv
import numpy as np
import requests
import templates
load_dotenv()

APIKEY = os.getenv("OPENAI_APIKEY")
API_ENDPOINT = 'https://api.openai.com/v1/chat/completions'


import warnings

warnings.filterwarnings("ignore")


class Processor():
    def __init__(self) -> None:
        self.vb = VoiceBot(api_key=APIKEY)


    def __speech_to_text(self, audio_path: str) -> str:
        transcript = self.vb.transcribe(audio_path)
        return transcript
    
    
    def __send_message(self, message):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(APIKEY)
        }
        data = {
            'model': 'gpt-3.5-turbo',  
            'messages': [{'role': 'user', 'content': message}],
        }
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return 'Error: {}'.format(response.text)
    

        
    def __calculate_call_duration(self, file_path: str) -> tuple[str, float]:
        
        audio, _ = librosa.load(file_path)
        
        seconds = librosa.get_duration(y = audio)

        return self.__process_duration(seconds), seconds


    def __process_duration(self, seconds: float) -> str:
        hours = math.floor(seconds / 3600)
        minutes = math.floor((seconds % 3600) / 60)
        seconds = round(seconds % 60, 2)

        return f"{hours:02d} Hours: {minutes:02d} Minutes: {seconds} Seconds"
    


    def __calculate_silence_ratio(self, audio_file: str) -> str:

        audio, sr = librosa.load(audio_file, sr=None)

        energy = librosa.feature.rms(y=audio)

        energy_db = librosa.amplitude_to_db(energy)

        silence_threshold_db = -60

        silent_segments = np.where(energy_db < silence_threshold_db, 1, 0)

        total_silence_duration = np.sum(silent_segments) / sr

        total_duration = librosa.get_duration(y=audio, sr=sr)
        # print(total_duration)

        silence_ratio = total_silence_duration / total_duration

        silence_ratio = f"{silence_ratio:.7f}"

        return silence_ratio
    



    def __first_call_resolution(self, audio_text: str) -> tuple[str, int]:

        prompt = templates.first_call_resolution(audio_text)

        response = self.__send_message(prompt).strip()

        if response[0] == "0":
            res = "UnSolved"
            return res, 0
        elif response[0] == "1":
            res = "Solved"
            return res, 1
        else:
            res = "NA"
            return res, 0
        
    def __customer_satisfaction_score(self, audio_text: str) -> float:

        prompt = templates.customer_satisfaction_score(audio_text)

        response = self.__send_message(prompt).strip()

        try:
            response = float(response)
            return round(response, 2)
        except:
            return float(0)
        
    
    def __call_transfer_rate(self, audio_text: str) -> tuple[str, float]:

        prompt = templates.call_transfer_rate(audio_text)

        response = self.__send_message(prompt).strip()


        if response[0] == "0":
            res = "Not Transferred"
            return res, 0
        elif response[0] == "1":
            res = "Transferred"
            return res, 1
        else:
            res = "NA"
            return res, 0
        

    def __error_rate(self, audio_text: str) -> int:

        prompt = templates.error_rate(audio_text)

        response = self.__send_message(prompt).strip()

        try:
            response = int(response)
            return response
        except:
            return 0








    def process(self, audio_folder_path: str) -> str:

        resolved_calls = 0
        total_calls = 0
        transferred_calls = 0
        total_call_duration = 0
        total_rating = 0
        total_silence_ratio = 0
        total_overcall_count = 0
        total_error_rate = 0

        final_res = ""
        
        
        for audio_paths in os.listdir(audio_folder_path):
            path = os.path.join(audio_folder_path, audio_paths)

            print(f"Processing {audio_paths}")
            total_calls += 1

            audio_text = self.__speech_to_text(path)

            #Inference
            duration_in_words, actual_duration = self.__calculate_call_duration(path)
            total_call_duration += actual_duration

            if actual_duration > 150:
                overcall = 1
            else:
                overcall = 0

            total_overcall_count += overcall



            call_resolve_status, call_resolve_value = self.__first_call_resolution(audio_text)
            resolved_calls += call_resolve_value


            rating = self.__customer_satisfaction_score(audio_text)
            total_rating += rating
            
            
            call_transfer_status, call_transfer_value = self.__call_transfer_rate(audio_text)
            transferred_calls += call_resolve_value

            silence_ratio = self.__calculate_silence_ratio(path)
            total_silence_ratio += float(silence_ratio)


            error_rate = self.__error_rate(audio_text)

            total_error_rate += error_rate

            final_res += f"Inference of {audio_paths}\n"
            final_res += "-----------------------------------------\n"
            final_res += f"Duration: {duration_in_words}\n" 
            final_res += f"First Call Resolution Status: {call_resolve_status}\n"
            final_res += f"First Call Resolution Value: {call_resolve_value}\n"
            final_res += f"Customer Satisfaction Rating: {rating}\n"
            final_res += f"Call Transfer Status: {call_transfer_status}\n"
            final_res += f"Call Transfer Value: {call_transfer_value}\n"
            final_res += f"Silence Ratio: {silence_ratio}\n"
            final_res += f"Error Rate: {error_rate}\n"

        
        average_call_duration = total_call_duration / total_calls
        average_rating = total_rating / total_calls
        resolved_calls_percentage = (resolved_calls / total_calls) * 100
        transferred_calls_percentage = (transferred_calls/ total_calls) * 100
        average_silence_ratio = (total_silence_ratio / total_calls) * 100
        overcall_percentage = (total_overcall_count / total_calls) * 100
        average_error_rate = (total_error_rate / total_calls)
        
        final_res += f"\nOverall Inference\n"
        final_res += f"-------------------------------------\n"
        final_res += f"Average Call Duration: {self.__process_duration(average_call_duration)}\n"
        final_res += f"Average Rating: {average_rating}\n"
        final_res += f"Resolved Calls Percentage: {resolved_calls_percentage}%\n"
        final_res += f"Transferred Calls Percentage: {transferred_calls_percentage}%\n"
        final_res += f"Average Silence Ratio: {average_silence_ratio}%\n"
        final_res += f"Overcall Percentage: {overcall_percentage}%\n"
        final_res += f"Average Error Rate: {average_error_rate}%\n"


        return final_res





        

if __name__ == "__main__":

    processor = Processor()


    res = processor.process(r"uploads\temp\extracted\Call Data Sample")

    with open("res.txt", "w", encoding = "utf8") as f:
        f.write(res)