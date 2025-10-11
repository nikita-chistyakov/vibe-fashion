'use client';
import { useRef, useState, useCallback, useEffect } from 'react';
import { getFrameFromStream } from '@/utils/getFrameFromStream';
import { useInputStore } from '@/libs/zustand/input';

export const CAMERA_WIDTH = 320;
export const CAMERA_HEIGHT = 180;
export const INTERVAL = 1000;

export function Camera() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const { setImages } = useInputStore();
  const [stream, setStream] = useState<MediaStream | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const showCameraFeed = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'user',
          width: CAMERA_WIDTH,
          height: CAMERA_HEIGHT,
        },
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setStream(stream);
      setIsPlaying(true);
    } catch (error) {
      console.error('Could not access camera:', error);
      setIsPlaying(false);
    }
  }, []);

  const generateFrame = useCallback(async () => {
    if (!videoRef.current || !setImages) {
      return;
    }
    const frame = await getFrameFromStream(videoRef.current);
    if (!frame) {
      console.error('Could not record video');
      return;
    }
    setImages([frame.base64]);
  }, [setImages]);

  useEffect(() => {
    if (!stream) {
      return;
    }
    if (isPlaying) {
      videoRef.current?.play();
    } else {
      videoRef.current?.pause();
    }
  }, [isPlaying, stream, videoRef]);

  useEffect(() => {
    if (isPlaying && stream) {
      generateFrame();
      intervalRef.current = setInterval(() => {
        generateFrame();
      }, INTERVAL);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }
  }, [generateFrame, isPlaying, stream]);

  return (
    <div
      className={`relative flex flex-col items-center justify-center mb-4 w-[${CAMERA_WIDTH}px] h-[${CAMERA_HEIGHT}px] border-2 border-black`}
    >
      <video
        ref={videoRef}
        autoPlay={isPlaying}
        playsInline
        width={CAMERA_WIDTH}
        height={CAMERA_HEIGHT}
        style={{ transform: 'scaleX(-1)' }}
      />
      <div className="absolute bottom-0 right-0 flex flex-row items-center justify-center gap-4">
        {!stream && (
          <button
            onClick={showCameraFeed}
            className={`border-2 border-green-500 p-2 bg-green-500 text-white rounded`}
          >
            📹
          </button>
        )}
      </div>
    </div>
  );
}
