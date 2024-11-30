import speech_recognition as sr
from queue import Queue
import threading
import time
import torch
from transformers import pipeline, AutoModelForCTC, AutoProcessor
import numpy as np


class VoiceRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_queue = Queue()
        self.text_queue = Queue()
        self.is_running = False

        # Whisper 모델 로드 (빠른 처리를 위해 'tiny' 버전 사용)
        self.speech_to_text = pipeline("automatic-speech-recognition",
                                       model="openai/whisper-tiny",
                                       chunk_length_s=30)

    def start_listening(self):
        """음성 인식 시작"""
        self.is_running = True
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.processing_thread = threading.Thread(target=self._process_audio)

        self.recording_thread.start()
        self.processing_thread.start()

    def stop_listening(self):
        """음성 인식 중지"""
        self.is_running = False
        self.recording_thread.join()
        self.processing_thread.join()

    def _record_audio(self):
        """오디오 녹음"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("음성 인식 준비 완료...")

            while self.is_running:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    self.audio_queue.put(audio)
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"녹음 중 오류 발생: {str(e)}")

    def _process_audio(self):
        """오디오 처리 및 텍스트 변환"""
        while self.is_running:
            if not self.audio_queue.empty():
                audio = self.audio_queue.get()
                try:
                    # 오디오 데이터를 WAV 형식으로 변환
                    wav_data = audio.get_wav_data()
                    # numpy array로 변환
                    audio_array = np.frombuffer(wav_data, dtype=np.int16)

                    # Whisper 모델로 음성 인식
                    result = self.speech_to_text(audio_array)
                    recognized_text = result["text"]

                    if recognized_text.strip():
                        self.text_queue.put(recognized_text)
                        print(f"인식된 텍스트: {recognized_text}")

                except Exception as e:
                    print(f"처리 중 오류 발생: {str(e)}")

            time.sleep(0.1)

    def get_recognized_text(self):
        """인식된 텍스트 반환"""
        if not self.text_queue.empty():
            return self.text_queue.get()
        return None