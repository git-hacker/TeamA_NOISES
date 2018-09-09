import os

import librosa
import numpy as np
from django.core.files import File
from keras.backend import clear_session
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Audio
from api.wavenet import wavenet
from apiserver.settings import MEDIA_ROOT


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    动态ModelSerializer, 接收参数`fields`, `exclude`来控制显示字段
    """

    def __init__(self, *args, **kwargs):
        # 需要移除 'fields' 和 'exclude' , superclass不接收该参数
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # 'fields'和'exclude'不能同时出现
        if fields is not None and exclude is not None:
            raise ValueError("'fields'和'exclude'不能同时出现")

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        # 移除不被包含的字段
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            not_allowed = set(exclude)
            for field_name in not_allowed:
                self.fields.pop(field_name)


class AudioSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'


def read_wav(path, fs=16000):
    data, _ = librosa.load(path, sr=fs)
    return np.trim_zeros(data)


def save_wav(path, data):
    librosa.output.write_wav(path, data, sr=16000)


def denoise(src):
    from oct2py import octave
    x = octave.feval('api/logmmse', np.trim_zeros(src), 16000)
    x = np.trim_zeros(x)
    return np.float32(np.squeeze(x))


class AudioViewset(viewsets.ModelViewSet):
    serializer_class = AudioSerializer
    queryset = Audio.objects.all().order_by('-timestamp')

    def create(self, request, *args, **kwargs):
        serializer = AudioSerializer(data=request.data)
        if serializer.is_valid():
            audio = Audio.objects.create(**serializer.validated_data)
            return Response(AudioSerializer(audio).data)
        return Response(serializer.errors, status=400)

    @action(detail=True)
    def denoise(self, _, pk=None):
        audio = Audio.objects.get(pk=pk)
        if not audio.denoised:
            print("denoising!")
            path = audio.raw_file.path
            wave = read_wav(path)
            denoised = denoise(wave)
            filename = 'de_' + audio.raw_file.name
            save_path = os.path.join(MEDIA_ROOT, filename)
            save_wav(save_path, denoised)
            f = open(save_path, 'rb')
            os.remove(save_path)
            audio.denoised.save(filename, File(f))
            f.close()
            return Response(audio.denoised.url)

        return Response(audio.denoised.url)

    @action(detail=True)
    def transform(self, _, pk=None):
        audio = Audio.objects.get(pk=pk)
        if not audio.denoised:
            return Response("此操作需先降噪", status=400)
        if not audio.transformed:
            path = audio.denoised.path
            wave = read_wav(path)
            raw, de = transform(wave)

            filename = 'tr_' + audio.raw_file.name
            save_path = os.path.join(MEDIA_ROOT, filename)
            save_wav(save_path, de)
            f = open(save_path, 'rb')
            os.remove(save_path)
            audio.transformed.save(filename, File(f))
            f.close()
            return Response(audio.transformed.url)

        return Response(audio.transformed.url)


def transform(wave):
    window_size = 4000
    shift = 4000
    def assemble():
        x = []
        for i in range(0, len(wave) - window_size, shift):
            x.append(wave[i : i + window_size])
        return np.array(x)

    print("[TRANSFORM] Preparing input data...\n")
    feed = assemble()
    print("[TRANSFORM] Loading neural network model...\n")
    clear_session()
    model = wavenet(window_size)
    model.load_weights('weights.h5')
    print("[TRANSFORM] Transforming audio data...\n")
    predictions = model.predict(np.expand_dims(feed, axis=2), batch_size=16)
    output = predictions.flatten()
    print("[TRANSFORM] Denoising transformed audio data...\n")
    denoised = denoise(output)
    print("[TRANSFORM] Transformation complete!\n")
    return output, denoised
